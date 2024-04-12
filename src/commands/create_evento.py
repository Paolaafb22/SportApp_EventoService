from .base_command import BaseCommannd
from ..models.evento import eventos, Eventoschema,eventosJsonSchema
from ..session import Session
from ..errors.errors import IncompleteParams, InvalidNombreError, EventosAlreadyExists

class CreateEventos(BaseCommannd):
  def __init__(self, data):
    self.data = data
  
  def execute(self):
    try:
      posted_Eventos = Eventoschema(
        only=('nombre', 'estado', 'url_imagen')
      ).load(self.data)
      print(posted_Eventos)
      
      if not self.verificar_datos(posted_Eventos["nombre"]):
        raise InvalidNombreError
      
      eventos = eventos(**posted_Eventos)
      session = Session()
      
      if self.eventos_exist(session, self.data['nombre']):
        session.close()
        raise EventosAlreadyExists()

      session.add(eventos)
      session.commit()

      new_eventos = eventosJsonSchema().dump(eventos)
      session.close()

      return new_eventos
        
    except TypeError as te:
      print("Error en el primer try:", str(te))
      raise IncompleteParams()
  
  def eventos_exist(self, session, nombre):
    return len(session.query(eventos).filter_by(nombre=nombre).all()) > 0
  
  def verificar_datos(self,nombre):
    if nombre and nombre.strip():
        return True
    else:
        return False