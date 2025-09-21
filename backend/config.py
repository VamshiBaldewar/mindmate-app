"""
Configuration settings for GathaFeed Backend
"""

import os
from typing import List

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'gathafeed-secret-key-2024')
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'gathafeed:'
    
    # Google Cloud Configuration
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', 'AIzaSyAqyOxS65ZeQz9r3zajaosNtShqZnbSqbs')
    PROJECT_ID = os.environ.get('PROJECT_ID', 'gathafeed-ai')
    REGION = os.environ.get('REGION', 'us-central1')
    
    # Database Configuration
    FIRESTORE_PROJECT_ID = os.environ.get('FIRESTORE_PROJECT_ID', PROJECT_ID)
    
    # Storage Configuration
    STORAGE_BUCKET_NAME = os.environ.get('STORAGE_BUCKET_NAME', 'gathafeed-storage')
    
    # CORS Configuration
    ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(',')
    
    # Development Settings
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
