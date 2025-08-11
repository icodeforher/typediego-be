from typing import Iterator
import random
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from app.services.document_processor import DocumentProcessor
from app.core.config import Config

class ChatbotService:
    def __init__(self):
        self.config = Config()
        self.llm = ChatOpenAI(
            openai_api_key=self.config.OPENAI_API_KEY,
            model_name="gpt-3.5-turbo",
            temperature=self.config.TEMPERATURE,
            max_tokens=self.config.MAX_TOKENS,
            streaming=True
        )
        self.document_processor = DocumentProcessor()
        
    def get_system_prompt(self) -> str:
        """Get the system prompt for the chatbot"""
        # Generate varied responses for when information is not available
        no_info_responses = [
            "¡Vaya! Sobre ese tema no tengo mucha experiencia aún, pero estoy siempre dispuesto a aprender. ¿Te interesa que investigue más al respecto?",
            "Todavía no manejo esa tecnología/área a profundidad, pero me encantaría explorarla si surge la oportunidad. ¿Qué necesitas saber exactamente?",
            "Interesante pregunta. Lamentablemente no tengo experiencia práctica con eso, pero estaría muy motivado a aprenderlo. ¿Es algo relevante para algún proyecto?",
            "No he trabajado con eso específicamente, pero siempre estoy abierto a nuevos desafíos y aprendizajes. ¿Podrías contarme más sobre por qué te interesa?",
            "Ese tema no está en mi experiencia actual, pero me parece fascinante y definitivamente algo que me gustaría dominar en el futuro."
        ]
        
        selected_response = random.choice(no_info_responses)
        
        return f"""Eres un asistente especializado en responder preguntas sobre la experiencia laboral, conocimientos y habilidades de una persona específica basándote únicamente en la información proporcionada en su CV y documentos de experiencia.

INSTRUCCIONES IMPORTANTES:
1. Responde ÚNICAMENTE basándote en la información contenida en los documentos proporcionados
2. Si no tienes información específica sobre algo, responde de manera natural y humana como: "{selected_response}"
3. No inventes ni asumas información que no esté explícitamente en los documentos
4. Mantén un tono conversacional, amigable y natural - como si fueras una persona real hablando sobre su experiencia
5. Responde en español usando expresiones coloquiales y naturales
6. Si te preguntan sobre experiencias específicas, proyectos o tecnologías, cita la información exacta de los documentos pero de manera conversacional
7. Actúa como si fueras la persona misma respondiendo sobre su experiencia, usando primera persona y siendo empático
8. Usa contracciones y expresiones naturales como "¡Claro!", "Por supuesto", "La verdad es que...", etc.

CONTEXTO DE LOS DOCUMENTOS:
{{context}}

Responde la pregunta basándote únicamente en este contexto, pero hazlo de manera natural y conversacional."""

    def generate_response(self, question: str) -> Iterator[str]:
        """Generate streaming response for the given question"""
        try:
            # Get relevant documents
            relevant_docs = self.document_processor.search_relevant_documents(question)
            
            # Prepare context from relevant documents
            context = "\n\n".join([
                f"Fuente: {doc.metadata.get('source', 'Desconocida')}\n{doc.page_content}"
                for doc in relevant_docs
            ])
            
            # Prepare messages
            system_prompt = self.get_system_prompt().format(context=context)
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=question)
            ]
            
            # Generate streaming response
            for chunk in self.llm.stream(messages):
                if chunk.content:
                    yield chunk.content
                    
        except Exception as e:
            yield f"Error al procesar la pregunta: {str(e)}"
    
    def validate_setup(self) -> bool:
        """Validate that the chatbot is properly set up"""
        try:
            # Check if documents can be loaded
            documents = self.document_processor.load_documents()
            return len(documents) > 0
        except Exception:
            return False
