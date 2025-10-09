from django.contrib import admin
from .models import PricingRule

@admin.register(PricingRule)
class PricingRuleAdmin(admin.ModelAdmin):
    list_display = ("id","name","scope","target_template","target_pattern","priority","stop","valid_from","valid_to","created_at")
    list_filter = ("scope","stop")
    search_fields = ("name",)
    readonly_fields = ("created_at",)
    fieldsets = (
        (None, {"fields": ("name","scope","target_template","target_pattern","priority","stop")}),
        ("Vigencia", {"fields": ("valid_from","valid_to")}),
        ("Lógica", {"fields": ("condition","action")}),
        ("Meta", {"fields": ("created_at",)}),
    )