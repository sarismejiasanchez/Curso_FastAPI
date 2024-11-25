from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

# Clase para representar los datos del Cliente
class Customer(BaseModel):
    """
    Modelo de datos para un cliente.

    Atributos:
    - name: Nombre del cliente.
    - description: Descripción opcional del cliente.
    - email: Dirección de correo electrónico válida.
    - age: Edad del cliente.
    """
    name: str
    description: str | None
    email: EmailStr
    age: int
    
# Inicializar la aplicación FastAPI
app = FastAPI()

# Diccionario de zonas horarias según los códigos ISO
country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima"
}

@app.get("/")
async def root():
    """
    Endpoint raíz de la aplicación.

    Retorna un mensaje simple de saludo.
    """
    return {"message": "Hola, Sara!"}


@app.get("/get_time/{iso_code}")
async def get_time(iso_code: str, format_12hr: bool = False):
    """
    Endpoint para obtener la hora actual en la zona horaria de un país.

    Parámetros:
    - iso_code: Código ISO del país (ejemplo: "CO", "MX").
    - format_12hr: Booleano que indica si se debe retornar la hora en formato de 12 horas (True) o 24 horas (False).

    Retorna:
    - Un diccionario con la hora actual formateada, el código ISO y la zona horaria.
    """
    
    # Convertir el código ISO a mayúsculas y validarlo
    iso = iso_code.upper()
    if iso not in country_timezones:
        raise HTTPException(status_code=400, detail="Código ISO no válido")
    
    # Obtener la zona horaria asociada al código ISO
    timezone_name = country_timezones.get(iso)
    try:
        timezone = ZoneInfo(timezone_name)
    except KeyError:
        raise HTTPException(status_code=500, detail="Zona horaria no encontrada")
    
    # Obtener la hora actual en la zona horaria especificada
    current_time = datetime.now(timezone)
    
    # Determinar el formato de la hora (12 o 24 horas)
    time_format = "%I:%M %p" if format_12hr else "%H:%M"
    formatted_time = current_time.strftime(time_format)
    
    return {
        "time": formatted_time,
        "iso_code": iso,
        "timezone": timezone_name
    }


@app.post("/customers")
async def create_customer(customer_data: Customer):
    """
    Endpoint para crear un cliente.

    Parámetros:
    - customer_data: Objeto JSON que contiene los datos del cliente.

    Retorna:
    - Los datos del cliente que se recibieron.
    """
    return customer_data
