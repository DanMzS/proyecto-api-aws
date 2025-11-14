from typing import List, Dict, Any

alumnos: List[Dict[str, Any]] = []
profesores: List[Dict[str, Any]] = []

# Generadores de IDs que ahora pueden ser establecidos externamente
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

def set_alumno_id(new_id: int) -> None:
    """Establece el siguiente ID de alumno si el proporcionado es mayor"""
    global _next_alumno_id
    if new_id >= _next_alumno_id:
        _next_alumno_id = new_id + 1

def set_profesor_id(new_id: int) -> None:
    """Establece el siguiente ID de profesor si el proporcionado es mayor"""
    global _next_profesor_id
    if new_id >= _next_profesor_id:
        _next_profesor_id = new_id + 1