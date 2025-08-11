from functools import wraps
from flask import request, jsonify, current_app

def api_key_required(f):
    """Decorator to require API key in headers"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get API key from headers
        api_key = request.headers.get('X-API-KEY')
        
        if not api_key:
            return jsonify({
                'error': 'API Key requerida',
                'message': 'Debe proporcionar una API key en el header X-API-KEY'
            }), 401
        
        # Get valid API keys from config
        from app.core.config import Config
        config = Config()
        valid_keys = config.API_KEYS
        
        if not valid_keys:
            return jsonify({
                'error': 'Configuración de autenticación no encontrada',
                'message': 'El servidor no tiene configuradas API keys válidas'
            }), 500
        
        if api_key not in valid_keys:
            return jsonify({
                'error': 'API Key inválida',
                'message': 'La API key proporcionada no es válida'
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

def require_auth_token(f):
    """Decorator to require authentication token in headers (legacy support)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from headers
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                'error': 'Token de autorización requerido',
                'message': 'Debe proporcionar un token de autorización en el header Authorization'
            }), 401
        
        # Extract token (support both "Bearer token" and just "token" formats)
        token = auth_header.replace('Bearer ', '') if auth_header.startswith('Bearer ') else auth_header
        
        # Get valid API keys from config
        from app.core.config import Config
        config = Config()
        valid_keys = config.API_KEYS
        
        if not valid_keys:
            return jsonify({
                'error': 'Configuración de autenticación no encontrada',
                'message': 'El servidor no tiene configuradas API keys válidas'
            }), 500
        
        if token not in valid_keys:
            return jsonify({
                'error': 'Token de autorización inválido',
                'message': 'El token proporcionado no es válido'
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function
