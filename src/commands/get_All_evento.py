from .base_command import BaseCommannd
from ..errors.errors import Unauthorized, InvalidParams, EventoNotFoundError
from ..dynamodb_evento import DynamoDbEvento

class GetAllEvento(BaseCommannd):
    def __init__(self):
        # No se necesita ningún parámetro en la inicialización para obtener todos los eventos
        pass
  
    def execute(self):
        # Llamar al método 'scan' en lugar de 'get_item' para obtener todos los eventos
        result = DynamoDbEvento().scan()

        if not result:
            # Si no se encuentran eventos, lanzar EventoNotFoundError o devolver un valor vacío, según tu preferencia
            raise EventoNotFoundError("No se encontraron eventos.")

        return result
