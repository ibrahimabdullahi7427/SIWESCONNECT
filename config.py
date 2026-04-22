import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'siwesconnect-secret-2025'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///siwesconnect.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False