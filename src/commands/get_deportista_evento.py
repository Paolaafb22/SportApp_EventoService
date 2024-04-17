from .base_command import BaseCommannd
from ..errors.errors import Unauthorized, InvalidParams, EventoNotFoundError
from ..dynamodb_deportista_evento import DynamoDbDeportistaEvento

class GetDeportistaEvento(BaseCommannd):
  def __init__(self, id_usuario):
    if id_usuario and id_usuario.strip():
      self.id_usuario = id_usuario
    else:
      raise InvalidParams()
  
  def execute(self):

    result  = DynamoDbDeportistaEvento().get_Item_usuario(self.id_usuario)
    if result is None:
      raise EventoNotFoundError()
    
    return result