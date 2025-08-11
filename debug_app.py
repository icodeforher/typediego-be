from app.services.document_processor import DocumentProcessor
from app.services.chatbot_service import ChatbotService
import os

def debug_document_loading():
    print("=== Debug Document Loading ===")
    
    # Test document processor
    processor = DocumentProcessor()
    documents = processor.load_documents()
    
    if documents:
        print(f"\n✓ Documentos cargados exitosamente: {len(documents)}")
        for i, doc in enumerate(documents):
            print(f"  Documento {i+1}:")
            print(f"    Fuente: {doc.metadata.get('source', 'N/A')}")
            print(f"    Tipo: {doc.metadata.get('type', 'N/A')}")
            print(f"    Contenido (primeros 100 chars): {doc.page_content[:100]}...")
    else:
        print("\n✗ No se cargaron documentos")
    
    # Test chatbot service
    print("\n=== Test Chatbot Service ===")
    try:
        chatbot = ChatbotService()
        is_valid = chatbot.validate_setup()
        print(f"Chatbot setup válido: {is_valid}")
        
        if is_valid:
            print("\n✓ Chatbot configurado correctamente")
        else:
            print("\n✗ Problema con la configuración del chatbot")
            
    except Exception as e:
        print(f"\n✗ Error inicializando chatbot: {e}")

if __name__ == "__main__":
    debug_document_loading()
