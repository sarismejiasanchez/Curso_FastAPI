# Clase para representar los datos del Cliente
from pydantic import BaseModel, EmailStr

class Customer(BaseModel):
    """
    Modelo de datos para un cliente.

    Atributos:
    - id (int): Identificador único del cliente.
    - name (str): Nombre del cliente.
    - description (str | None): Descripción opcional del cliente.
    - email (EmailStr): Dirección de correo electrónico válida del cliente.
    - age (int): Edad del cliente.
    """
    id: int
    name: str
    description: str | None
    email: EmailStr
    age: int

class Transaction(BaseModel):
    """
    Modelo de datos para una transacción.

    Atributos:
    - id (int): Identificador único de la transacción.
    - ammount (int): Monto asociado a la transacción.
    - description (str): Descripción de la transacción.
    """
    id: int
    ammount: int
    description: str

class Invoice(BaseModel):
    """
    Modelo de datos para una factura.

    Atributos:
    - id (int): Identificador único de la factura.
    - customer (Customer): Información del cliente asociado a la factura.
    - transactions (list[Transaction]): Lista de transacciones incluidas en la factura.
    - total (int): Total calculado manualmente para la factura.
    """
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int
    
    @property
    def ammount_total(self) -> int:
        """
        Calcula el monto total de todas las transacciones incluidas en la factura.

        Returns:
        - int: La suma total de los montos de las transacciones.
        """
        return sum(transaction.ammount for transaction in self.transactions)
    