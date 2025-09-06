import math

from .models import *
SVG_WIDTH = 1000
SVG_HEIGHT = 1000

def flip_y(y, height=SVG_HEIGHT):
    return height - y

def degrees_to_radians(deg):
    return math.radians(deg)


def polar_to_cartesian(cx, cy, radius, angle_deg):
    angle_rad = degrees_to_radians(angle_deg)
    x = cx + radius * math.cos(angle_rad)
    y = cy + radius * math.sin(angle_rad)
    return x, y

def dxf_line_to_svg(e, dwg):
    x1, y1, z1 = e.dxf.start
    x2, y2, z2 = e.dxf.end
    return dwg.line(start=(x1, flip_y(y1)), end=(x2, flip_y(y2)), stroke='black')

def dxf_polyline_to_svg(e, dwg):
    points = [(x, flip_y(y)) for x, y, *_ in e.get_points()]
    return dwg.polyline(points=points, stroke='blue', fill='none')

def dxf_text_to_svg(e, dwg):
    x, y, z = e.dxf.insert
    text_str = e.dxf.text
    return dwg.text(text_str, insert=(x, flip_y(y)), font_size=10)

def convert_arc(e, dwg):
    cx, cy, cz = e.dxf.center
    r = e.dxf.radius
    start_angle = e.dxf.start_angle
    end_angle = e.dxf.end_angle

    # Ajuste para SVG
    start = polar_to_cartesian(cx, cy, r, end_angle)
    end = polar_to_cartesian(cx, cy, r, start_angle)
    large_arc = 1 if (end_angle - start_angle) % 360 > 180 else 0
    sweep_flag = 0  # DXF es sentido antihorario

    path = f"M {start[0]},{flip_y(start[1])} A {r},{r} 0 {large_arc},{sweep_flag} {end[0]},{flip_y(end[1])}"
    return dwg.path(d=path, fill='none', stroke='green')


def parte_to_svg_element(parte, dwg):
    grupo = dwg.g(id=parte.nombre_parte.replace(" ", "_").lower())
    if not parte.geometria:
        return grupo

    for elemento in parte.geometria:
        tipo = elemento.get("tipo")
        if tipo == "polyline":
            puntos = [(x, flip_y(y)) for x, y in elemento["puntos"]]
            grupo.add(dwg.polyline(points=puntos, stroke=elemento.get("color", "black"), fill="none"))
        elif tipo == "line":
            x1, y1 = elemento["x1"], flip_y(elemento["y1"])
            x2, y2 = elemento["x2"], flip_y(elemento["y2"])
            grupo.add(dwg.line(start=(x1, y1), end=(x2, y2), stroke=elemento.get("color", "black")))
        elif tipo == "path":
            grupo.add(dwg.path(d=elemento["d"], stroke=elemento.get("color", "black"), fill="none"))
        elif tipo == "text":
            x, y = elemento["x"], flip_y(elemento["y"])
            grupo.add(dwg.text(elemento["contenido"], insert=(x, y), font_size=elemento.get("size", 10)))
    return grupo

def generar_svg_para_patron(patron_id):
    patron = PatronBase.objects.get(id=patron_id)
    dwg = svgwrite.Drawing(size=(SVG_WIDTH, SVG_HEIGHT))
    for parte in patron.partes.all():
        grupo_svg = parte_to_svg_element(parte, dwg)
        dwg.add(grupo_svg)
    svg_string = dwg.tostring()
    print(f"SVG generado correctamente")
    return svg_string

def convert_dxf_to_svg(dxf_path):
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()
    dwg = svgwrite.Drawing(size=(SVG_WIDTH, SVG_HEIGHT))
    for block in doc.blocks:
        if block.name.startswith('*'):  # Ignorar bloques anónimos internos
            continue
        group = dwg.g(id=block.name)
        for entity in block:
            if entity.dxftype() == 'LINE':
                group.add(dxf_line_to_svg(entity, dwg))
            elif entity.dxftype() == 'LWPOLYLINE':
                group.add(dxf_polyline_to_svg(entity, dwg))
            elif entity.dxftype() == 'TEXT':
                group.add(dxf_text_to_svg(entity, dwg))
            elif entity.dxftype() == 'ARC':
                group.add(convert_arc(entity, dwg))
        dwg.add(group)
    for entity in msp:
        if entity.dxftype() == 'LINE':
            dwg.add(dxf_line_to_svg(entity, dwg))
        elif entity.dxftype() == 'LWPOLYLINE':
            dwg.add(dxf_polyline_to_svg(entity, dwg))
        elif entity.dxftype() == 'TEXT':
            dwg.add(dxf_text_to_svg(entity, dwg))
        elif entity.dxftype() == 'ARC':
            dwg.add(convert_arc(entity, dwg))
            
    svg_string = dwg.tostring()
    print(f"SVG generado")
    return svg_string
