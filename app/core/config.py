import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    API_KEYS = os.environ.get('API_KEYS', '').split(',') if os.environ.get('API_KEYS') else []
    
    # Paths for data files
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    CV_PDF_PATH = os.path.join(BASE_DIR, 'data', 'cv.pdf')
    EXPERIENCE_TXT_PATH = os.path.join(BASE_DIR, 'data', 'experience.txt')
    
    # LangChain settings
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    MAX_TOKENS = 500
    TEMPERATURE = 0.1  # Low temperature for accuracy
