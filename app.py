import json
from flask import Flask, request, jsonify
from validators import validar_alumno, validar_profesor
from errors import register_error_handlers, NotFoundError, ValidationError
from storage import alumnos, profesores, next_alumno_id, next_profesor_id

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
    ok, errs = validar_alumno(payload)
    if not ok:
        raise ValidationError(errs)
    alumno_creado = {
        'id': next_alumno_id(),
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
    ok, errs = validar_profesor(payload)
    if not ok:
        raise ValidationError(errs)
    profesor_creado = {
        'id': next_profesor_id(),
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

@app.post('/_echo')
def echo():
    return jsonify({
        "is_json": request.is_json,
        "json": request.get_json(silent=True),
        "raw": request.get_data(cache=False, as_text=True),
        "headers": {k: v for k, v in request.headers.items()}
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)