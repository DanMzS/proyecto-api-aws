from flask import jsonify

class NotFoundError(Exception):
    pass

class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors

def register_error_handlers(app):
    @app.errorhandler(NotFoundError)
    def handlle_not_found(err):
        return jsonify({"error": "Recurso no encontrado"}), 404
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(err: ValidationError):
        return jsonify({"errors": err.errors}), 400
    
    @app.errorhandler(Exception)
    def handle_generic(err):
        return jsonify({"error": "Error interno del servidor"}), 500