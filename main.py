from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import FastAPI, HTTPException
from models import Customer, Transaction, Invoice
    
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
    - iso_code (str): Código ISO del país (ejemplo: "CO", "MX").
    - format_12hr (bool, opcional): Booleano que indica si se debe retornar la hora en formato de 12 horas (True) o 24 horas (False). 
    En formato de 12 horas, se incluye el sufijo AM/PM para indicar si es antes o después del mediodía. 
    Por defecto, es False (formato de 24 horas).

    Retorna:
    - dict: Diccionario con los siguientes campos:
        - time (str): Hora actual formateada.
        - iso_code (str): Código ISO del país.
        - timezone (str): Nombre de la zona horaria correspondiente al país.

    Excepciones:
    - HTTPException 400: Si el código ISO proporcionado no es válido.
    - HTTPException 500: Si no se encuentra la zona horaria asociada al código ISO.
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

@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    """
    Endpoint para crear una transacción.

    Parámetros:
    - transaction_data: Objeto JSON que contiene los datos de la transacción.

    Retorna:
    - Los datos de la transacción que se recibieron.
    """
    return transaction_data

@app.post("/invoices")
async def create_invoices(invoices_data: Invoice):
    """
    Crea una factura y calcula el total dinámicamente.

    Parámetros:
    - invoice_data (Invoice): Objeto JSON que representa una factura.

    Retorna:
    - La factura con el total calculado basado en las transacciones.
    """
    return {
        "id": invoices_data.id,
        "customer": invoices_data.customer,
        "transactions": invoices_data.transactions,
        "total": invoices_data.ammount_total  # Usar la propiedad calculada
        }