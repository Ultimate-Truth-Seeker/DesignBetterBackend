# ecommerce/pricing_engine.py
from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

from django.utils import timezone
from django.db.models import Q

from patronaje.models import Configuration
from ecommerce.models import PricingRule, PricingRuleScope

Number = Union[int, float, Decimal]


# ---------- utilidades ----------
def _to_decimal(x: Number) -> Decimal:
    if isinstance(x, Decimal):
        return x
    try:
        return Decimal(str(x))
    except Exception:
        return Decimal("0")


def _quantize(amount: Decimal) -> Decimal:
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _get_in_context(ctx: Dict[str, Any], dotted: str, default: Any = None) -> Any:
    current: Any = ctx
    for part in dotted.split("."):
        if isinstance(current, dict):
            current = current.get(part, default)
        else:
            current = getattr(current, part, default)
    return current


# ---------- condiciones ----------
def _eval_predicate(pred: Dict[str, Any], ctx: Dict[str, Any]) -> bool:
    op = pred.get("op")
    field = pred.get("field")
    value = pred.get("value")
    left = _get_in_context(ctx, field, None)

    if op in ("==", "eq"):
        return left == value
    if op in ("!=", "ne"):
        return left != value
    if op in (">", "gt"):
        return _to_decimal(left) > _to_decimal(value)
    if op in (">=", "ge"):
        return _to_decimal(left) >= _to_decimal(value)
    if op in ("<", "lt"):
        return _to_decimal(left) < _to_decimal(value)
    if op in ("<=", "le"):
        return _to_decimal(left) <= _to_decimal(value)

    if op == "in":
        try:
            return left in value
        except TypeError:
            return False
    if op == "not_in":
        try:
            return left not in value
        except TypeError:
            return True
    if op == "contains":
        left_val = left if left is not None else ""
        try:
            return value in left_val
        except TypeError:
            return str(value) in str(left_val)

    if op == "exists":
        return left is not None
    if op == "isnull":
        return left is None
    if op == "startswith":
        return str(left).startswith(str(value))
    if op == "endswith":
        return str(left).endswith(str(value))
    return False


def _eval_condition(cond: Dict[str, Any], ctx: Dict[str, Any]) -> bool:
    if not cond:
        return True
    if "all" in cond:
        return all(_eval_condition(c, ctx) for c in cond["all"])
    if "any" in cond:
        return any(_eval_condition(c, ctx) for c in cond["any"])
    if "not" in cond:
        return not _eval_condition(cond["not"], ctx)
    return _eval_predicate(cond, ctx)


# ---------- acciones ----------
def _apply_action(action: Dict[str, Any], price: Decimal) -> Tuple[Decimal, Decimal, str]:
    """
    Devuelve (nuevo_precio, delta, label). Soporta:
      - {"set_price": 49.99}
      - {"add_pct": 0.12}
      - {"add_fixed": 2.5}
      - {"set_min_price": 39.99}
    """
    label = action.get("label") or ""
    if "set_price" in action:
        target = _quantize(_to_decimal(action["set_price"]))
        delta = target - price
        return target, _quantize(delta), label or "set_price"

    if "add_pct" in action:
        pct = _to_decimal(action["add_pct"])
        delta = _quantize(price * pct)
        return _quantize(price + delta), delta, label or f"add_pct {pct}"

    if "add_fixed" in action:
        delta = _quantize(_to_decimal(action["add_fixed"]))
        return _quantize(price + delta), delta, label or "add_fixed"

    if "set_min_price" in action:
        minimum = _quantize(_to_decimal(action["set_min_price"]))
        if price < minimum:
            delta = minimum - price
            return minimum, _quantize(delta), label or "set_min_price"
        return price, Decimal("0.00"), label or "set_min_price(noop)"

    return price, Decimal("0.00"), label or "noop"


# ---------- contexto ----------
def _get_pattern_from_template(tpl: Any) -> Any:
    for attr in ("pattern_base", "patron_base", "pattern"):
        if hasattr(tpl, attr):
            return getattr(tpl, attr)
    return None


def _collect_context(configuration: Configuration) -> Dict[str, Any]:
    tpl = getattr(configuration, "template", None)
    pat = _get_pattern_from_template(tpl) if tpl else None
    return {
        "template": {
            "id": getattr(tpl, "id", None),
            "code": getattr(tpl, "code", None),
            "name": getattr(tpl, "name", None),
            "category": getattr(tpl, "category", None),
        },
        "pattern": {
            "id": getattr(pat, "id", None),
            "code": getattr(pat, "code", None),
            "name": getattr(pat, "name", None),
        },
        "selected_options": getattr(configuration, "selected_options", {}) or {},
        "resolved_params": getattr(configuration, "resolved_params", {}) or {},
        "material_assignments": getattr(configuration, "material_assignments", {}) or {},
        "state": getattr(configuration, "state", None),
        "measurement_source": getattr(configuration, "measurement_source", None),
        "currency": getattr(configuration, "currency", "USD"),
    }


# ---------- selección de reglas ----------
def _applicable_rules(
    configuration: Configuration,
    when=None,
    include_global: bool = False,
    extra_qs: Optional[Iterable[PricingRule]] = None,
) -> Iterable[PricingRule]:
    """
    Por defecto SOLO reglas de la plantilla/patrón de la Configuration.
    Si include_global=True, también agrega scope=global.
    Compatible con:
      - Modelo con FKs: target_template / target_pattern
      - Modelo con un entero target_id + scope
    """
    when = when or timezone.now()
    tpl = getattr(configuration, "template", None)
    tpl_id = getattr(tpl, "id", None)
    pat = _get_pattern_from_template(tpl) if tpl else None
    pattern_id = getattr(pat, "id", None)

    base_q = Q()
    base_q &= (Q(valid_from__isnull=True) | Q(valid_from__lte=when))
    base_q &= (Q(valid_to__isnull=True) | Q(valid_to__gte=when))

    field_names = {f.name for f in PricingRule._meta.get_fields()}

    # Construir filtro según esquema real:
    q = Q()
    if "target_template" in field_names:
        q |= Q(scope=PricingRuleScope.TEMPLATE, target_template=tpl)
    if "target_pattern" in field_names:
        q |= Q(scope=PricingRuleScope.PATTERN, target_pattern_id=pattern_id)

    # Soporte para un único campo "target_id" (int) o "target" (FK con *_id implícito)
    if "target_id" in field_names:
        # Nota: si el modelo realmente define "target" como FK, el campo de columna será "target_id"
        q |= Q(scope=PricingRuleScope.TEMPLATE, target_id=tpl_id)
        q |= Q(scope=PricingRuleScope.PATTERN, target_id=pattern_id)
    if "target" in field_names:
        # por si el campo FK se llama "target" (Django añade "target_id" a nivel de columna)
        q |= Q(scope=PricingRuleScope.TEMPLATE, target_id=tpl_id)
        q |= Q(scope=PricingRuleScope.PATTERN, target_id=pattern_id)

    if include_global:
        q |= Q(scope=PricingRuleScope.GLOBAL)

    if extra_qs is not None:
        try:
            return extra_qs.order_by("priority", "id")
        except Exception:
            return extra_qs

    return PricingRule.objects.filter(base_q & q).order_by("priority", "id")


# ---------- API principal ----------
def compute_price_for_configuration(
    configuration: Configuration,
    rules: Optional[Iterable[PricingRule]] = None,
    include_global: bool = False,
    persist: bool = False,
) -> Dict[str, Any]:
    """
    price = subtotal
    for rule in rules_applicables_sorted:
        if eval(condition, configuration):
            price = apply(action, price)
            if rule.stop: break
    Devuelve breakdown y (opcional) persiste en Configuration.
    """
    ctx = _collect_context(configuration)

    # Base/subtotal inicial
    existing_breakdown = getattr(configuration, "cost_breakdown", {}) or {}
    base_amount = existing_breakdown.get("base", None)
    if base_amount is None:
        for attr in ("subtotal", "base_price"):
            if hasattr(configuration, attr) and getattr(configuration, attr) is not None:
                base_amount = getattr(configuration, attr)
                break
    price = _quantize(_to_decimal(base_amount if base_amount is not None else 0))

    # Reglas a aplicar
    rules_iter = rules if rules is not None else _applicable_rules(
        configuration, include_global=include_global
    )

    lines: List[Dict[str, Any]] = []
    for rule in rules_iter:
        if _eval_condition(rule.condition or {}, ctx):
            new_price, delta, label = _apply_action(rule.action or {}, price)
            new_price, delta = _quantize(new_price), _quantize(delta)
            lines.append(
                {
                    "rule_id": rule.id,
                    "name": rule.name,
                    "scope": rule.scope,
                    "action": rule.action,
                    "label": label,
                    "delta": str(delta),
                    "price_after": str(new_price),
                    "matched": True,
                }
            )
            price = new_price
            if getattr(rule, "stop", False) or (isinstance(rule.action, dict) and rule.action.get("stop") is True):
                break
        else:
            lines.append(
                {
                    "rule_id": rule.id,
                    "name": rule.name,
                    "scope": rule.scope,
                    "action": rule.action,
                    "matched": False,
                }
            )

    breakdown = {
        "base": str(_quantize(_to_decimal(base_amount or 0))),
        "lines": lines,
        "final": str(_quantize(price)),
        "currency": getattr(configuration, "currency", "USD"),
    }

    if persist:
        setattr(configuration, "cost_breakdown", breakdown)
        if hasattr(configuration, "price_total"):
            setattr(configuration, "price_total", _quantize(price))
            update_fields = ["cost_breakdown", "price_total"]
        elif hasattr(configuration, "total_price"):
            setattr(configuration, "total_price", _quantize(price))
            update_fields = ["cost_breakdown", "total_price"]
        else:
            update_fields = ["cost_breakdown"]
        if hasattr(configuration, "updated_at"):
            update_fields.append("updated_at")
        configuration.save(update_fields=update_fields)

    return breakdown


__all__ = ["compute_price_for_configuration"]