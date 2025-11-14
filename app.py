import json
from flask import Flask, request, jsonify
from validators import validar_alumno, validar_profesor
from errors import register_error_handlers, NotFoundError, ValidationError
from storage import alumnos, profesores, set_alumno_id, set_profesor_id

def get_json_or_empty():
    # 1) Intento normal
    data = request.get_json(silent=True)
    if isinstance(data, dict):
        return data

    # 2) Fallback: leer bytes crudos y parsear como UTF-8 (JSON estándar)
    raw_bytes = request.get_data(cache=False)  # <-- bytes, no texto
    if raw_bytes:
        try:
            return json.loads(raw_bytes)  # json.loads acepta bytes (asume UTF-8)
        except Exception:
            # Último intento: decodificar explícitamente y reintentar
            try:
                return json.loads(raw_bytes.decode('utf-8'))
            except Exception:
                pass

    # 3) Fallback para formularios con 'json='
    if request.form and 'json' in request.form:
        try:
            return json.loads(request.form['json'])
        except Exception:
            pass

    return {}

app = Flask(__name__)
register_error_handlers(app)

# Alumnos
@app.get('/alumnos')
def list_alumnos():
    return jsonify(alumnos), 200

@app.get('/alumnos/<int:item_id>')
def get_alumno(item_id: int):
    for a in alumnos:
        if a['id'] == item_id:
            return jsonify(a), 200
    raise NotFoundError()

@app.post('/alumnos')
def create_alumno():
    payload = get_json_or_empty()
    
    # Si viene con 'id' en el payload, usarlo; si no, generar uno nuevo
    alumno_id = None
    if 'id' in payload:
        try:
            alumno_id = int(payload['id'])
        except (ValueError, TypeError):
            pass
    
    ok, errs = validar_alumno(payload)
    if not ok:
        raise ValidationError(errs)
    
    # Si no hay ID, generar uno basado en la matrícula para hacerlo más único
    if alumno_id is None:
        # Usar un hash simple de la matrícula para generar un ID único
        matricula_str = str(payload['matricula'])
        alumno_id = abs(hash(matricula_str)) % 1000000
        # Si ya existe, buscar uno libre
        while any(a['id'] == alumno_id for a in alumnos):
            alumno_id = (alumno_id + 1) % 1000000
    
    set_alumno_id(alumno_id)
    
    alumno_creado = {
        'id': alumno_id,
        'nombres': payload['nombres'].strip(),
        'apellidos': payload['apellidos'].strip(),
        'matricula': payload['matricula'].strip(),
        'promedio': float(payload['promedio']),
    }
    alumnos.append(alumno_creado)
    return jsonify(alumno_creado), 201

@app.put('/alumnos/<int:item_id>')
def update_alumno(item_id: int):
    payload = get_json_or_empty()
    ok, errs = validar_alumno(payload)
    if not ok:
        raise ValidationError(errs)
    for idx, a in enumerate(alumnos):
        if a['id'] == item_id:
            alumno_actualizado = {
                'id': item_id,
                'nombres': payload['nombres'].strip(),
                'apellidos': payload['apellidos'].strip(),
                'matricula': payload['matricula'].strip(),
                'promedio': float(payload['promedio']),
            }
            alumnos[idx] = alumno_actualizado
            return jsonify(alumno_actualizado), 200
    raise NotFoundError()

@app.delete('/alumnos/<int:item_id>')
def delete_alumno(item_id: int):
    for idx, a in enumerate(alumnos):
        if a['id'] == item_id:
            alumnos.pop(idx)
            return jsonify({"deleted": True}), 200
    raise NotFoundError()

@app.delete('/alumnos')
def delete_alumnos_without_id():
    # DELETE sin ID debe retornar 404
    raise NotFoundError()

# Profesores
@app.get('/profesores')
def list_profesores():
    return jsonify(profesores), 200

@app.get('/profesores/<int:item_id>')
def get_profesor(item_id: int):
    for p in profesores:
        if p['id'] == item_id:
            return jsonify(p), 200
    raise NotFoundError()

@app.post('/profesores')
def create_profesor():
    payload = get_json_or_empty()
    
    # Si viene con 'id' en el payload, usarlo
    profesor_id = None
    if 'id' in payload:
        try:
            profesor_id = int(payload['id'])
        except (ValueError, TypeError):
            pass
    
    ok, errs = validar_profesor(payload)
    if not ok:
        raise ValidationError(errs)
    
    # Si no hay ID, generar uno basado en el numeroEmpleado
    if profesor_id is None:
        num_emp_str = str(payload['numeroEmpleado'])
        profesor_id = abs(hash(num_emp_str)) % 1000000
        while any(p['id'] == profesor_id for p in profesores):
            profesor_id = (profesor_id + 1) % 1000000
    
    set_profesor_id(profesor_id)
    
    profesor_creado = {
        'id': profesor_id,
        'numeroEmpleado': payload['numeroEmpleado'].strip(),
        'nombres': payload['nombres'].strip(),
        'apellidos': payload['apellidos'].strip(),
        'horasClase': int(payload['horasClase']),
    }
    profesores.append(profesor_creado)
    return jsonify(profesor_creado), 201

@app.put('/profesores/<int:item_id>')
def update_profesor(item_id: int):
    payload = get_json_or_empty()
    ok, errs = validar_profesor(payload)
    if not ok:
        raise ValidationError(errs)
    for idx, p in enumerate(profesores):
        if p['id'] == item_id:
            profesores[idx] = {
                'id': item_id,
                'numeroEmpleado': payload['numeroEmpleado'].strip(),
                'nombres': payload['nombres'].strip(),
                'apellidos': payload['apellidos'].strip(),
                'horasClase': int(payload['horasClase']),
            }
            return jsonify(profesores[idx]), 200
    raise NotFoundError()

@app.delete('/profesores/<int:item_id>')
def delete_profesor(item_id: int):
    for idx, p in enumerate(profesores):
        if p['id'] == item_id:
            profesores.pop(idx)
            return jsonify({"deleted": True}), 200
    raise NotFoundError()

@app.delete('/profesores')
def delete_profesores_without_id():
    # DELETE sin ID debe retornar 404
    raise NotFoundError()

@app.post('/_echo')
def echo():
    return jsonify({
        "is_json": request.is_json,
        "json": request.get_json(silent=True),
        "raw": request.get_data(cache=False, as_text=True),
        "headers": {k: v for k, v in request.headers.items()}
    }), 200

# Manejador para rutas no encontradas (404 en lugar de 500)
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Recurso no encontrado"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)