import uuid
from .base_command import BaseCommannd
from ..models.deportista_evento import DeportistaEvento
from ..errors.errors import IncompleteParams, InvalidNombreError, EventoAlreadyExistsInUser
from ..dynamodb_deportista_evento import DynamoDbDeportistaEvento

class CreateDeportaistaEvento(BaseCommannd):
  def __init__(self, data):
    self.data = data
  
  def execute(self):
    try:
      
      posted_evento = DeportistaEvento(self.data["id_usuario"],self.data['id_evento'], self.data['fecha_suscripcion'], 
                                           self.data['estado_suscripcion'])
            
      print(posted_evento)
      '''
      if not self.verificar_datos(self.data['nombre']):
         raise InvalidNombreError
      '''
      if self.evento_exist(self.data["id_usuario"],self.data['id_evento']):
        raise EventoAlreadyExistsInUser()

      DynamoDbDeportistaEvento().insert_item(posted_evento)

      return posted_evento
        
    except TypeError as te:
      print("Error en el primer try:", str(te))
      raise IncompleteParams()
  
  def evento_exist(self, id_usuario, id_evento):
    result = DynamoDbDeportistaEvento().get_Item_usuario(id_usuario, id_evento)
    if result is None:
      return False
    else:
      return True
  '''    
  def verificar_datos(self,nombre):
    if nombre and nombre.strip():
        return True
    else:
        return False
  '''