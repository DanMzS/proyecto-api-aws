from dataclasses import dataclass
from typing import Optional

@dataclass
class Alumno:
    id: int
    nombres: str
    apellidos: str
    matricula: str
    promedio: float


@dataclass
class Profesor:
    id: int
    numeroEmpleado: str
    nombres: str
    apellidos: str
    horasClase: int