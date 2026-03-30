import os

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DATABASE_URL = os.environ.get("DATABASE_URL")
    DEBUG = False
    TESTING = False

class Development(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = True

class Production(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False

# Configuration dictionary to easily access different configurations
config = {
    "development": Development,
    "production": Production,
    "default": Development
}