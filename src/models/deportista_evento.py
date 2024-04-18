from dataclasses import dataclass
from datetime import datetime

@dataclass
class DeportistaEvento:
    id_usuario: str
    id_evento: str
    fecha_suscripcion: datetime
    estado_suscripcion: bool
    