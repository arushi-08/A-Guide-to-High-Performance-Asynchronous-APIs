import os
from pathlib import Path
import urllib.parse as urlparse


SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

class BaseConfig:
    """Base configuration"""

    BASE_DIR = Path(__file__).parent.parent

    TESTING = False
    MONGO_TRACK_MODIFICATIONS = False
    MONGO_DATABASE_URI = urlparse.urlparse(
        "mongodb://flask_celery:flask_celery@mongodb:27017/flask_celery?authSource=admin"
    )
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
    CELERY_RESULT_BACKEND = os.environ.get(
        "CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0"
    )


class DevelopmentConfig(BaseConfig):
    """Development configuration"""

    DEBUG = True


class ProductionConfig(BaseConfig):
    """Production configuration"""

    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
