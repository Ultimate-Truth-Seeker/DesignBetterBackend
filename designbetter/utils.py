# tu_app/utils.py
from django.core.signing import Signer
signer = Signer()

def generar_token_activacion(correo_electronico):
    return signer.sign(correo_electronico)