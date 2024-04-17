from .base_command import BaseCommannd
from ..errors.errors import Unauthorized, InvalidParams, EventoNotFoundError
from ..dynamodb_evento import DynamoDbEvento

class GetEvento(BaseCommannd):
  def __init__(self, evento_id):
    if evento_id and evento_id.strip():
      self.evento_id = evento_id
    else:
      raise InvalidParams()
  
  def execute(self):

    result  = DynamoDbEvento().get_item(self.evento_id)
    if result is None:
      raise EventoNotFoundError()
    
    return result