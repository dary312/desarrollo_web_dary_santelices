import re
import filetype
from datetime import datetime, timedelta

def validate_sector(value):
    if value is None or value.strip() == "":
        return True
    return len(value) <= 100

def validate_nombre(value):
    return value and len(value) <= 200 and len(value) >= 3

def validate_email(value):
    if value is None or value.strip() == "":
        return False 
    if len(value) >= 100:
        return False
    regex = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$"
    return re.match(regex, value) is not None

def validate_celular(value):
    if value is None or value.strip() == "":
        return True 
    regex = r"^\+\d{3}\.\d{8}$"
    return re.match(regex, value) is not None

def validate_red_social(value):
    if value is None or value.strip() == "":
        return True 
    return value and len(value) <= 50 and len(value) >= 4

def validate_tipo(value):
    if value == "perro" or value == "gato":
        return True
    return False

def validate_cantidad(value):
    if value is None or value.strip() == "":
        return False
    else: 
        int_value = int(value)
        return int_value >= 1 

def validate_edad(value):
    if value is None or value.strip() == "":
        return False
    else: 
        int_value = int(value)
        return int_value >= 1 

def validate_unidad(value):
    if value == "a" or value == "m":
        return True
    return False

def validate_fecha(value, fecha_minima):
    if value is None:
        return False
    return value >= fecha_minima
    

def validate_descripcion(value):
    if value is None or value.strip() == "":
        return True 
    return len(value) <= 500

def validate_fotos(lista_archivos):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}

    if not lista_archivos or not isinstance(lista_archivos, list):
        return False

    fotos_validas = 0

    for archivo in lista_archivos:

        if archivo.filename == "":
            continue

        contenido = archivo.read()
        archivo.seek(0)

        tipo = filetype.guess(contenido)
        if tipo is None:
            return False
        if tipo.extension not in ALLOWED_EXTENSIONS:
            return False
        if tipo.mime not in ALLOWED_MIMETYPES:
            return False

        fotos_validas += 1


    return fotos_validas > 0