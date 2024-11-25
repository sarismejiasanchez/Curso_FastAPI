from fastapi import FastAPI, HTTPException

import zoneinfo
from datetime import datetime

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hola, Sara!"}

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima"
}

"""
Endpoint par obtener la hora en formato de 12 o 24 horas según el código ISO.

Parámetros:
- iso_code: Código ISO del país (ej., "CO", "MX").
- format_12hr: Booleano para especificar formato de 12 horas (True) o 24 horas (False).
    
Retorna:
- La hora actual en la zona horaria especificada. 
"""

@app.get("/get_time/{iso_code}")
async def get_time(iso_code: str, format_12hr: bool = False):
    
    # Validar el código ISO
    iso = iso_code.upper()
    if iso not in country_timezones:
        raise HTTPException(status_code=500, detail="Código ISO no válido")
    
    # Obtener Zona Horaria
    timezone_name = country_timezones.get(iso)
    try:
        timezone = zoneinfo.ZoneInfo(timezone_name)
    except KeyError:
        raise HTTPException(status_code=500, detail="Zona horaria no encontrada")
    
    # Obtener la hora actual en la zona horaria especificada
    current_time = datetime.now(timezone)
    
    # Determinar el formato de la hora
    time_format = "%I:%M %p" if format_12hr else "%H:%M"
    formatted_time = current_time.strftime(time_format)
    
    return {
        "time": formatted_time,
        "iso_code": iso,
        "timezone": timezone_name
    }