from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import FastAPI, HTTPException
from models import Customer, CustomerCreate, Transaction, Invoice
    
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

# Base de datos simulada
db_customers: list[Customer] = []
db_invoices: list[Invoice] = []

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
    - format_12hr (bool, opcional): Si es True, retorna la hora en formato 12 horas (incluyendo AM/PM). 
    Por defecto es False (formato 24 horas).

    Retorna:
    - dict: Hora actual formateada, código ISO, y nombre de la zona horaria.

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
    

@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate):
    """
    Crea un nuevo cliente.

    Parámetros:
    - customer_data (CustomerCreate): Datos del cliente.

    Retorna:
    - Customer: Cliente creado con un identificador único.
    """
    
    # Genera un nuevo ID único para el cliente. 
    # Si la lista de clientes no está vacía, toma el ID del último cliente y le suma 1; 
    # de lo contrario, asigna 1 como ID inicial.
    new_id = (db_customers[-1].id + 1) if db_customers else 1
    
    # Valida y crea una instancia del modelo Customer a partir de los datos proporcionados, 
    # asegurándose de que cumplan con las reglas definidas en el modelo
    customer = Customer.model_validate(customer_data.model_dump())
    customer.id = new_id
    db_customers.append(customer)
    return customer


@app.get("/customers", response_model=list[Customer])
async def list_customer():
    """
    Lista todos los clientes registrados.

    Retorna:
    - list[Customer]: Lista de clientes registrados en la base de datos.
    """
    return db_customers

@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    """
    Crea una nueva transacción.

    Parámetros:
    - transaction_data (Transaction): Datos de la transacción.

    Retorna:
    - Transaction: Transacción creada.
    """
    return transaction_data

@app.post("/invoices")
async def create_invoices(invoice_data: Invoice):
    """
    Crea una factura y calcula el total basado en las transacciones.

    Parámetros:
    - invoice_data (Invoice): Datos de la factura.

    Retorna:
    - Invoice: Factura creada con el total calculado.
    """
    # Crea una nueva instancia del modelo Invoice con los datos proporcionados:
    # - Asigna un nuevo ID basado en el último ID en db_invoices, incrementándolo en 1, 
    # o utiliza 1 si db_invoices está vacío.
    # - Asigna al cliente los datos del cliente asociados a la factura (invoice_data.customer).
    # - Asigna las transacciones incluidas en la factura (invoice_data.transactions).
    invoice = Invoice(
        id=(db_invoices[-1].id + 1) if db_invoices else 1,
        customer=invoice_data.customer,
        transactions=invoice_data.transactions,
    )
    db_invoices.append(invoice)
    return {
        "id": invoice.id,
        "customer": invoice.customer,
        "transactions": invoice.transactions,
        "total": invoice.ammount_total
    }