from dataclasses import dataclass
from datetime import datetime
from typing import List
from enum import Enum

class Nivel(Enum):
    BASICO = "Básico"
    INTERMEDIO = "Intermedio"
    AVANZADO = "Avanzado"

@dataclass
class Evento:
    id_evento: str
    nombre: str
    fecha_evento: datetime
    id_socio: str
    descripcion:str
    nivel: Nivel
    estado: bool
