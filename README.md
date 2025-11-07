# 🌐 Entrega 1 – API REST con Flask  
**Materia:** AWS Cloud Foundations  
**Autor:** Daniel Méndez Sierra
**Lenguaje:** Python (Flask)  
**Despliegue:** Amazon EC2 (VPC pública)

---

## 📘 Descripción general

Esta aplicación implementa una **API REST en memoria** con Flask que gestiona dos entidades:

- **Alumnos:** `id`, `nombres`, `apellidos`, `matricula`, `promedio`  
- **Profesores:** `id`, `numeroEmpleado`, `nombres`, `apellidos`, `horasClase`

El proyecto cumple con los requisitos solicitados en la primera entrega del curso **AWS Cloud Foundations**:

- Endpoints CRUD completos (`GET`, `POST`, `PUT`, `DELETE`)
- Validaciones de tipo de dato y campos vacíos
- Respuestas **JSON** con códigos HTTP correctos (200, 201, 400, 404, 500)
- Sin base de datos (almacenamiento en memoria)
- Despliegue en **instancia EC2 (Amazon Linux)** dentro de una **VPC pública**
- Creación de una **AMI** al finalizar

---

## ⚙️ Requisitos previos

- Python 3.11+  
- Flask 3.0+  
- Git  
- AWS CLI configurado (para el despliegue)

Instalar dependencias:
```bash
python -m pip install -r requirements.txt
```
Ejecutar localmente
```bash
python app.py
```

La API estará disponible en:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

## 🧩 Endpoints disponibles

### 📚 Alumnos
| Método | Endpoint | Descripción |
|--------|-----------|-------------|
| GET | `/alumnos` | Lista todos los alumnos |
| GET | `/alumnos/<id>` | Consulta un alumno por ID |
| POST | `/alumnos` | Crea un nuevo alumno |
| PUT | `/alumnos/<id>` | Actualiza un alumno existente |
| DELETE | `/alumnos/<id>` | Elimina un alumno |

### 👨‍🏫 Profesores
| Método | Endpoint | Descripción |
|--------|-----------|-------------|
| GET | `/profesores` | Lista todos los profesores |
| GET | `/profesores/<id>` | Consulta un profesor por ID |
| POST | `/profesores` | Crea un nuevo profesor |
| PUT | `/profesores/<id>` | Actualiza un profesor existente |
| DELETE | `/profesores/<id>` | Elimina un profesor |

---

## 🧪 Pruebas con `curl`

### Obtener lista vacía
```bash
curl -i http://127.0.0.1:8000/alumnos
```

### Crear un alumno
```bash
curl -i -H "Content-Type: application/json; charset=utf-8" \
  --data-binary '{"nombres":"Ana","apellidos":"Lopez","matricula":"A001","promedio":95.5}' \
  http://127.0.0.1:8000/alumnos
```
### Actualizar un alumno
```bash
curl -i -X PUT -H "Content-Type: application/json; charset=utf-8" \
  --data-binary '{"nombres":"Ana","apellidos":"L\u00f3pez","matricula":"A001","promedio":96.0}' \
  http://127.0.0.1:8000/alumnos/1
```
### Eliminar un alumno
```bash
curl -i -X DELETE http://127.0.0.1:8000/alumnos/1
```
> Todos los endpoints devuelven JSON con los códigos HTTP correspondientes (200, 201, 400, 404).

# 📋 Códigos de estado HTTP esperados:
|  Código | Significado           | Cuándo ocurre                                |
| :-----: | --------------------- | -------------------------------------------- |
| **200** | OK                    | Lectura, actualización o eliminación exitosa |
| **201** | Created               | Registro creado exitosamente                 |
| **400** | Bad Request           | Datos inválidos o campos vacíos              |
| **404** | Not Found             | Recurso no encontrado                        |
| **500** | Internal Server Error | Error inesperado del servidor                |

---

 # 🧾 Ejemplo de respuesta JSON:
 ## POST /alumnos
```json
{
  "id": 1,
  "nombres": "Ana",
  "apellidos": "Lopez",
  "matricula": "A001",
  "promedio": 95.5
}
```

## Error 400
```json
{
  "errors": {
    "promedio": "promedio es requerido (float)."
  }
}
```
---
# 💡 Notas
La aplicación mantiene los datos en memoria, por lo que al reiniciar el servidor se pierden los registros.

Para asegurar compatibilidad con caracteres acentuados, se recomienda usar siempre:
```bash
Content-Type: application/json; charset=utf-8
```

# Estructura del proyecto
```
aws-entrega1-flask/
├── app.py                 # Archivo principal de la aplicación Flask
├── models.py              # Definición de las clases Alumno y Profesor
├── storage.py             # Almacenamiento en memoria de alumnos y profesores
├── validators.py          # Funciones de validación para alumnos y profesores
├── errors.py              # Manejo de errores personalizados
├── requirements.txt       # Dependencias del proyecto
├── run.sh                 # Script para ejecutar la aplicación
└── README.md              # Documentación del proyecto
``` 