from flask import Flask, request, jsonify
from validators import validar_alumno, validar_profesor
from errors import register_error_handlers, NotFoundError, ValidationError
from storage import alumnos, profesores, next_alumno_id, next_profesor_id

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
    payload = request.get_json(silent=True) or {}
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
    payload = request.get_json(silent=True) or {}
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
    payload = request.get_json(silent=True) or {}
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
    payload = request.get_json(silent=True) or {}
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)