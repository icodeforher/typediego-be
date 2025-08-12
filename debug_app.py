from app.services.document_processor import DocumentProcessor
from app.services.chatbot_service import ChatbotService
import os

def debug_document_loading():
    print("=== Debug Document Loading ===")
    
    # Test document processor
    processor = DocumentProcessor()
    documents = processor.load_documents()
    
    if documents:
        print(f"\n✓ Documents loaded successfully: {len(documents)}")
        for i, doc in enumerate(documents):
            print(f"  Document {i+1}:")
            print(f"    Source: {doc.metadata.get('source', 'N/A')}")
            print(f"    Type: {doc.metadata.get('type', 'N/A')}")
            print(f"    Content (first 100 chars): {doc.page_content[:100]}...")
    else:
        print("\n✗ No documents loaded")
    
    # Test chatbot service
    print("\n=== Test Chatbot Service ===")
    try:
        chatbot = ChatbotService()
        is_valid = chatbot.validate_setup()
        print(f"Chatbot setup valid: {is_valid}")
        
        if is_valid:
            print("\n✓ Chatbot configured correctly")
        else:
            print("\n✗ Problem with chatbot configuration")
            
    except Exception as e:
        print(f"\n✗ Error initializing chatbot: {e}")

if __name__ == "__main__":
    debug_document_loading()
