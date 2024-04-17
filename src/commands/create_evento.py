import uuid
from .base_command import BaseCommannd
#from ..models.entrenamiento import Entrenamiento
from ..models.evento import Evento, DeportistaEvento
from ..errors.errors import IncompleteParams, InvalidNombreError, EventoAlreadyExists
from ..dynamodb_evento import DynamoDbEvento

class CreateEvento(BaseCommannd):
  def __init__(self, data):
    self.data = data
  
  def execute(self):
    try:
      
      posted_evento = Evento(str(uuid.uuid4()),self.data['nombre'], self.data['fecha_evento'], 
                                           self.data['id_socio'],self.data['descripcion'],self.data['nivel'],
                                           self.data['estado'])
            
      print(posted_evento)
      
      if not self.verificar_datos(self.data['nombre']):
         raise InvalidNombreError
      
      if self.evento_exist(self.data['nombre']):
        raise EventoAlreadyExists()

      DynamoDbEvento().insert_item(posted_evento)

      return posted_evento
        
    except TypeError as te:
      print("Error en el primer try:", str(te))
      raise IncompleteParams()
  
  def evento_exist(self, nombre):
    result = DynamoDbEvento().get_Item_nombre(nombre)
    if result is None:
      return False
    else:
      return True
      
  def verificar_datos(self,nombre):
    if nombre and nombre.strip():
        return True
    else:
        return False