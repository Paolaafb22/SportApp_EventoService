from .base_command import BaseCommannd
from ..errors.errors import IncompleteParams, InvalidParams, RecomendationsNotFoundError
from ..dynamodb_evento import DynamoDbEvento

class BuscarEventosRecomendados(BaseCommannd):
    def __init__(self, data):
        self.data = data
        if self.data['ciudad'] and self.data['ciudad'].strip():
            self.ciudad = self.data['ciudad']
        else:
            raise InvalidParams()

    def execute(self):
        try:
                    
            print(self.data)
            
            result = DynamoDbEvento().recomendar_items(self.ciudad,self.data['fecha_prevista'])
            if result is None:
                raise RecomendationsNotFoundError()
            
            return result
                
        except TypeError as te:
            print("Error en el primer try:", str(te))
        raise IncompleteParams()