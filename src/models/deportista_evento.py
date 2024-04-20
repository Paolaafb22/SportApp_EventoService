from dataclasses import dataclass
from datetime import datetime
from .evento import Evento
@dataclass
class DeportistaEvento:
    id_usuario_evento: str
    id_usuario: str
    id_evento: str
    fecha_suscripcion: datetime
    estado_suscripcion: bool
    
@dataclass
class DeportistaEventosJson:
    id_usuario_evento: str
    id_usuario: str
    id_evento: str
    fecha_suscripcion: datetime
    estado_suscripcion: bool
    evento: Evento   