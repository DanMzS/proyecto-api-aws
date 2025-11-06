from typing import List, Dict, Any

alumnos: List[Dict[str, Any]] = []
profesores: List[Dict[str, Any]] = []

# Generadores sencillos de IDs
_next_alumno_id = 1
_next_profesor_id = 1

def next_alumno_id() -> int:
    global _next_alumno_id
    nid = _next_alumno_id
    _next_alumno_id += 1
    return nid

def next_profesor_id() -> int:
    global _next_profesor_id
    nid = _next_profesor_id
    _next_profesor_id += 1
    return nid