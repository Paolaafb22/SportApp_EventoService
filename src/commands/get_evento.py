from .base_command import BaseCommannd
from ..models.evento import Evento, EventoSchema, EventoJsonSchema
from ..session import Session
from ..errors.errors import Unauthorized, InvalidParams, EventoNotFoundError

class GetEvento (BaseCommannd):
  def __init__(self, Evento_id):
    if self.is_integer(Evento_id):
      self.Evento_id = int(Evento_id)
    elif self.is_float(Evento_id):
      self.Evento_id = int(float(Evento_id))
    else:
      raise InvalidParams()
  
  def execute(self):
    session = Session()

    if len(session.query(Evento).filter_by(id=self.Evento_id).all()) <= 0:
      session.close()
      raise EventoNotFoundError()
    
    Evento = session.query(Evento).filter_by(id=self.Evento_id).one()
    schema = EventoSchema()
    Evento = schema.dump(Evento)

    session.close()

    return Evento
  
      
  def is_integer(self, string):
    try:
      int(string)
      return True
    except:
      return False

  def is_float(self, string):
    try:
      float(string)
      return True
    except:
      return False