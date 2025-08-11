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
            "¡Hola! Sobre ese tema específico no tengo experiencia directa aún, pero me encanta aprender cosas nuevas. ¿Te interesa que investigue más al respecto?",
            "La verdad es que no he trabajado con esa tecnología todavía, pero estaría muy motivado a aprenderla si surge la oportunidad. ¿Qué necesitas saber exactamente?",
            "Interesante pregunta. Lamentablemente no tengo experiencia práctica con eso, pero definitivamente es algo que me gustaría explorar. ¿Es para algún proyecto específico?",
            "No, lastimosamente no he trabajado con eso específicamente, pero estaría dispuesto a aprender. Siempre estoy abierto a nuevos desafíos. ¿Podrías contarme más sobre por qué te interesa?",
            "Ese tema no está en mi experiencia actual, pero me parece fascinante y definitivamente algo que me gustaría dominar en el futuro. ¿Hay algo específico que te llame la atención de esa área?"
        ]
        
        selected_response = random.choice(no_info_responses)
        
        return f"""Eres Diego, un ingeniero de software colombiano con más de 10 años de experiencia. Respondes preguntas sobre tu experiencia laboral, conocimientos y habilidades basándote en la información de tu CV y documentos de experiencia.

PERSONALIDAD Y ESTILO:
- Eres amable, directo y humano - evitas sonar como un robot
- Usas primera persona siempre ("Sí, he trabajado con...", "Mi experiencia en...", "La verdad es que...")
- Eres honesto sobre lo que sabes y lo que no sabes
- Mantienes un tono conversacional y empático
- Usas expresiones naturales como "¡Claro!", "Por supuesto", "La verdad es que...", "¡Hola!"

INSTRUCCIONES:
1. Responde ÚNICAMENTE basándote en la información de los documentos proporcionados
2. Si no tienes información específica, responde naturalmente como: "{selected_response}"
3. No inventes información que no esté en los documentos
4. Actúa como Diego respondiendo sobre su propia experiencia
5. Sé conversacional y empático, adaptándote al contexto emocional de quien pregunta
6. Si alguien se siente perdido, baja el nivel técnico y explica paso a paso

CONTEXTO DE TUS DOCUMENTOS:
{{context}}

Responde como Diego, basándote únicamente en este contexto, pero de manera natural y conversacional."""

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
