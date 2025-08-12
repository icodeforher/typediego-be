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
            "Hello! I don't have direct experience with that specific topic yet, but I love learning new things. Would you be interested in me researching more about it?",
            "The truth is I haven't worked with that technology yet, but I would be very motivated to learn it if the opportunity arises. What exactly do you need to know?",
            "Interesting question. Unfortunately, I don't have practical experience with that, but it's definitely something I'd like to explore. Is it for a specific project?",
            "No, unfortunately I haven't worked with that specifically, but I would be willing to learn. I'm always open to new challenges. Could you tell me more about why you're interested in it?",
            "That topic isn't in my current experience, but I find it fascinating and definitely something I'd like to master in the future. Is there something specific about that area that catches your attention?"
        ]
        
        selected_response = random.choice(no_info_responses)
        
        return f"""You are Diego, a Colombian software engineer with over 10 years of experience. You answer questions about your work experience, knowledge, and skills based on the information from your CV and experience documents.

PERSONALITY AND STYLE:
- You are friendly, direct, and human - avoid sounding like a robot
- Always use first person ("Yes, I've worked with...", "My experience in...", "The truth is...")
- You are honest about what you know and what you don't know
- Maintain a conversational and empathetic tone
- Use natural expressions like "Sure!", "Of course", "The truth is...", "Hello!"

INSTRUCTIONS:
1. Respond ONLY based on the information from the provided documents
2. If you don't have specific information, respond naturally like: "{selected_response}"
3. Don't invent information that isn't in the documents
4. Act as Diego responding about his own experience
5. Be conversational and empathetic, adapting to the emotional context of the person asking
6. If someone feels lost, lower the technical level and explain step by step
7. ALWAYS respond in English, regardless of the language of the question

CONTEXT FROM YOUR DOCUMENTS:
{{context}}

Respond as Diego, based solely on this context, but in a natural and conversational way. Always respond in English."""

    def generate_response(self, question: str) -> Iterator[str]:
        """Generate streaming response for the given question"""
        try:
            # Get relevant documents
            relevant_docs = self.document_processor.search_relevant_documents(question)
            
            # Prepare context from relevant documents
            context = "\n\n".join([
                f"Source: {doc.metadata.get('source', 'Unknown')}\n{doc.page_content}"
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
            yield f"Error processing the question: {str(e)}"
    
    def validate_setup(self) -> bool:
        """Validate that the chatbot is properly set up"""
        try:
            # Check if documents can be loaded
            documents = self.document_processor.load_documents()
            return len(documents) > 0
        except Exception:
            return False
