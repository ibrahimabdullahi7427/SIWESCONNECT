import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'siwesconnect-secret-2025'
    
    uri = os.environ.get('DATABASE_URL') or 'sqlite:///siwesconnect.db'
if uri.startswith('postgres://'):
    uri = uri.replace('postgres://', 'postgresql+psycopg://', 1)
elif uri.startswith('postgresql://'):
    uri = uri.replace('postgresql://', 'postgresql+psycopg://', 1)
SQLALCHEMY_DATABASE_URI = uri