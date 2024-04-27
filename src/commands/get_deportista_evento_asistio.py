from .base_command import BaseCommannd
from ..errors.errors import Unauthorized, InvalidParams, EventoNotFoundError
from ..dynamodb_deportista_evento import DynamoDbDeportistaEvento
from datetime import datetime, timedelta

class GetDeportistaAsistioEvento(BaseCommannd):
  def __init__(self, id_usuario, dias):
    if id_usuario and id_usuario.strip():
      self.id_usuario = id_usuario
    else:
      raise InvalidParams()
    
    if dias and dias.strip() and dias.isdigit():
        self.dias = int(dias)
    else:
        raise InvalidParams()
  
  def execute(self):
    fecha_desde = (datetime.now() - timedelta(days=self.dias)).strftime('%Y-%m-%d')
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    result  = DynamoDbDeportistaEvento().get_eventos_asistio_ultimos_dias(self.id_usuario, fecha_desde, fecha_actual)
    
    return { 'asistio': len(result) }
