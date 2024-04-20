from .base_command import BaseCommannd
from ..errors.errors import Unauthorized, InvalidParams, EventoNotFoundError
from ..dynamodb_deportista_evento import DynamoDbDeportistaEvento
from ..dynamodb_evento import DynamoDbEvento
from ..models.deportista_evento import DeportistaEventosJson
from ..models.evento import Evento

class GetDeportistaEvento(BaseCommannd):
  def __init__(self, id_usuario):
    if id_usuario and id_usuario.strip():
      self.id_usuario = id_usuario
    else:
      raise InvalidParams()
  
  def execute(self):
    resultadoJson = []
    result  = DynamoDbDeportistaEvento().get_Item_usuario(self.id_usuario)
    if result is None:
      raise EventoNotFoundError()
    for item in result:      
      deportistaEvento = DeportistaEventosJson(item.id_usuario_evento,item.id_usuario,item.id_evento,item.fecha_suscripcion, item.estado_suscripcion,None)
      item_evento = DynamoDbEvento().get_item(item.id_evento)
      if item_evento:
        evento = Evento(item_evento.id_evento,item_evento.nombre,item_evento.lugar,item_evento.fecha_evento,item_evento.id_socio,item_evento.descripcion,item_evento.nivel,item_evento.estado)
        deportistaEvento.evento = evento
      resultadoJson.append(deportistaEvento)
    
    return resultadoJson