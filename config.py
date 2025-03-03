import os
import secrets
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

class Config:
    # Generate a secure random secret key
    SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(32))
    
    # Ensure instance folder exists
    instance_path = os.path.join(basedir, 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(instance_path, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Google Cloud settings
    GOOGLE_CLOUD_PROJECT = os.environ.get('GOOGLE_CLOUD_PROJECT', 'steganography-450607')
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', 
        os.path.join(basedir, 'gcloud.json'))
    BUCKET_NAME = os.environ.get('BUCKET_NAME', 'steganography-app-bucket')