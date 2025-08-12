import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from app.core.config import Config

class DocumentProcessor:
    def __init__(self):
        self.config = Config()
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.config.OPENAI_API_KEY)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.CHUNK_SIZE,
            chunk_overlap=self.config.CHUNK_OVERLAP,
            length_function=len,
        )
        self.vectorstore = None
        
    def load_documents(self) -> List[Document]:
        """Load and process PDF and TXT documents"""
        documents = []
        
        print(f"Looking for files in:")
        print(f"  CV: {self.config.CV_PDF_PATH}")
        print(f"  Experience: {self.config.EXPERIENCE_TXT_PATH}")
        
        # Load PDF (CV)
        if os.path.exists(self.config.CV_PDF_PATH):
            print(f"✓ CV file found")
            try:
                pdf_loader = PyPDFLoader(self.config.CV_PDF_PATH)
                pdf_docs = pdf_loader.load()
                for doc in pdf_docs:
                    doc.metadata['source'] = 'CV'
                    doc.metadata['type'] = 'professional_experience'
                documents.extend(pdf_docs)
                print(f"✓ CV processed: {len(pdf_docs)} pages")
            except Exception as e:
                print(f"✗ Error processing CV: {e}")
        else:
            print(f"✗ CV file not found at: {self.config.CV_PDF_PATH}")
        
        # Load TXT (Experience details)
        if os.path.exists(self.config.EXPERIENCE_TXT_PATH):
            print(f"✓ Experience file found")
            try:
                txt_loader = TextLoader(self.config.EXPERIENCE_TXT_PATH, encoding='utf-8')
                txt_docs = txt_loader.load()
                for doc in txt_docs:
                    doc.metadata['source'] = 'Experience Details'
                    doc.metadata['type'] = 'personal_insights'
                documents.extend(txt_docs)
                print(f"✓ Experience processed: {len(txt_docs)} documents")
            except Exception as e:
                print(f"✗ Error processing Experience: {e}")
        else:
            print(f"✗ Experience file not found at: {self.config.EXPERIENCE_TXT_PATH}")
        
        print(f"Total documents loaded: {len(documents)}")
        return documents
    
    def create_vectorstore(self) -> FAISS:
        """Create vector store from documents"""
        documents = self.load_documents()
        
        if not documents:
            raise ValueError("No documents found. Please ensure CV PDF and experience TXT files exist in the data folder.")
        
        # Split documents into chunks
        texts = self.text_splitter.split_documents(documents)
        
        # Create vector store
        self.vectorstore = FAISS.from_documents(texts, self.embeddings)
        return self.vectorstore
    
    def get_vectorstore(self) -> FAISS:
        """Get existing vectorstore or create new one"""
        if self.vectorstore is None:
            self.vectorstore = self.create_vectorstore()
        return self.vectorstore
    
    def search_relevant_documents(self, query: str, k: int = 4) -> List[Document]:
        """Search for relevant documents based on query"""
        vectorstore = self.get_vectorstore()
        return vectorstore.similarity_search(query, k=k)
