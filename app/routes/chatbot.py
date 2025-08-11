from flask import Blueprint, request, jsonify, Response
from app.services.chatbot_service import ChatbotService
from app.utils.auth import api_key_required
import json

chatbot_bp = Blueprint('chatbot', __name__)

# Initialize chatbot service
chatbot_service = ChatbotService()

@chatbot_bp.route('/chat', methods=['POST'])
@api_key_required
def chat():
    """Main chat endpoint that returns streaming responses"""
    try:
        # Get question from request
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({
                'error': 'Pregunta requerida',
                'message': 'Debe proporcionar una pregunta en el campo "question"'
            }), 400
        
        question = data['question'].strip()
        if not question:
            return jsonify({
                'error': 'Pregunta vacía',
                'message': 'La pregunta no puede estar vacía'
            }), 400
        
        # Validate chatbot setup
        if not chatbot_service.validate_setup():
            return jsonify({
                'error': 'Configuración incompleta',
                'message': 'No se encontraron documentos para procesar. Asegúrese de que existan los archivos CV.pdf y experience.txt en la carpeta data/'
            }), 500
        
        def generate():
            """Generator function for streaming response"""
            try:
                for chunk in chatbot_service.generate_response(question):
                    # Format each chunk as Server-Sent Events
                    yield f"data: {json.dumps({'content': chunk, 'type': 'chunk'})}\n\n"
                
                # Send completion signal
                yield f"data: {json.dumps({'content': '', 'type': 'done'})}\n\n"
                
            except Exception as e:
                # Send error in stream format
                error_msg = f"Error durante la generación: {str(e)}"
                yield f"data: {json.dumps({'content': error_msg, 'type': 'error'})}\n\n"
        
        # Return streaming response
        return Response(
            generate(),
            mimetype='text/plain',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type, X-API-KEY',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            }
        )
        
    except Exception as e:
        return jsonify({
            'error': 'Error interno del servidor',
            'message': f'Error al procesar la solicitud: {str(e)}'
        }), 500

@chatbot_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        is_ready = chatbot_service.validate_setup()
        return jsonify({
            'status': 'healthy' if is_ready else 'not_ready',
            'message': 'Chatbot está funcionando correctamente' if is_ready else 'Documentos no encontrados',
            'documents_loaded': is_ready
        }), 200 if is_ready else 503
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error en el health check: {str(e)}'
        }), 500

@chatbot_bp.route('/chat', methods=['OPTIONS'])
def chat_options():
    """Handle CORS preflight requests"""
    return '', 200, {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, X-API-KEY',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
    }
