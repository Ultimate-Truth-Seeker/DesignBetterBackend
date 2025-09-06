# tu_app/utils.py
from django.core.signing import Signer
import svgwrite, ezdxf, math
from django.db import connection

signer = Signer()
def generar_token_activacion(correo_electronico):
    return signer.sign(correo_electronico)
