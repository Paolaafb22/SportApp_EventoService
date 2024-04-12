from marshmallow import  Schema, fields
from sqlalchemy import Column, String, Boolean
from .model import Model, Base
from datetime import datetime, timedelta

class Evento(Model, Base):
  __tablename__ = 'eventos'

  nombre = Column(String)
  fecha = Column(String)
  lugar = Column(String)
  descripcion = Column(String)
  nivel = Column(String)

  def __init__(self, nombre, fecha, lugar,descripcion,nivel):
    Model.__init__(self)
    self.nombre = nombre
    self.fecha = fecha
    self.lugar = lugar
    self.descripcion = descripcion
    self.nivel = nivel
    
class EventoSchema(Schema):
  id = fields.Number()
  nombre = fields.Str()
  fecha = fields.Str()
  lugar = fields.Str()
  descripcion = fields.Str()
  nivel = fields.Str()


class servicioLogisticoJsonSchema(Schema):
  id = fields.Number()
  nombre = fields.Str()
  estado = fields.Bool()
  url_imagen = fields.Str()
  expireAt = fields.DateTime()
  createdAt = fields.DateTime()
  
  
