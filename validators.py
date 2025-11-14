from typing import Tuple, Dict, Any

# Devuelve (válido: bool, errores: dict)

def validar_alumno(payload: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
    errores = {}

    # Requeridos: nombres, apellidos, matricula, promedio
    if 'nombres' not in payload or not isinstance(payload['nombres'], str) or not payload['nombres'].strip():
        errores['nombres'] = "El campo 'nombres' es obligatorio y debe ser una cadena no vacía."

    if 'apellidos' not in payload or not isinstance(payload['apellidos'], str) or not payload['apellidos'].strip():
        errores['apellidos'] = "El campo 'apellidos' es obligatorio y debe ser una cadena no vacía."

    if 'matricula' not in payload or not isinstance(payload['matricula'], str) or not payload['matricula'].strip():
        errores['matricula'] = "El campo 'matricula' es obligatorio y debe ser una cadena no vacía."

    if 'promedio' not in payload:
        errores['promedio'] = "El campo 'promedio' es obligatorio."
    else:
        try:
            val = float(payload['promedio'])
            # Validar que el promedio esté en un rango razonable (0-100)
            if val < 0 or val > 100:
                errores['promedio'] = 'promedio debe estar entre 0 y 100.'
        except (ValueError, TypeError):
            errores['promedio'] = 'promedio debe ser numérico (float).'
    
    return (len(errores) == 0, errores)

def validar_profesor(payload: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
    errores = {}

    # Requeridos: numeroEmpleado, nombres, apellidos, horasClase
    if 'numeroEmpleado' not in payload:
        errores['numeroEmpleado'] = "El campo 'numeroEmpleado' es obligatorio."
    else:
        # Aceptar tanto string como número para numeroEmpleado
        val = payload['numeroEmpleado']
        if isinstance(val, (int, float)):
            # Es un número, convertir a string
            payload['numeroEmpleado'] = str(val)
        elif isinstance(val, str):
            if not val.strip():
                errores['numeroEmpleado'] = "El campo 'numeroEmpleado' no puede estar vacío."
        else:
            errores['numeroEmpleado'] = "El campo 'numeroEmpleado' debe ser una cadena o número."

    if 'nombres' not in payload or not isinstance(payload['nombres'], str) or not payload['nombres'].strip():
        errores['nombres'] = "El campo 'nombres' es obligatorio y debe ser una cadena no vacía."

    if 'apellidos' not in payload or not isinstance(payload['apellidos'], str) or not payload['apellidos'].strip():
        errores['apellidos'] = "El campo 'apellidos' es obligatorio y debe ser una cadena no vacía."

    if 'horasClase' not in payload:
        errores['horasClase'] = "El campo 'horasClase' es obligatorio."
    else:
        try:
            val = int(payload['horasClase'])
            if val < 0:
                errores['horasClase'] = 'horasClase debe ser entero >= 0.'
        except (ValueError, TypeError):
            errores['horasClase'] = 'horasClase debe ser entero.'
    
    return (len(errores) == 0, errores)