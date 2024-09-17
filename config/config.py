# config/config.py
import os
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pythonjsonlogger import jsonlogger

class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')

class FrontendConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('FRONTEND_DATABASE_URL', 'sqlite:///frontend_library.db')

class BackendConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('BACKEND_DATABASE_URL', 'sqlite:///backend_library.db')

class FrontendDevelopmentConfig(FrontendConfig):
    DEBUG = True

class FrontendProductionConfig(FrontendConfig):
    DEBUG = False
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

class BackendDevelopmentConfig(BackendConfig):
    DEBUG = True

class BackendProductionConfig(BackendConfig):
    DEBUG = False
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Centralized mapping of configs
Config = {
    'frontend_development': FrontendDevelopmentConfig,
    'frontend_production': FrontendProductionConfig,
    'backend_development': BackendDevelopmentConfig,
    'backend_production': BackendProductionConfig
}

def get_config():
    """Load the appropriate config based on environment variables."""
    app_role = os.getenv('APP_ROLE', 'frontend')
    env = os.getenv('FLASK_ENV', 'development')
    
    config_key = f"{app_role}_{env}"
    return Config.get(config_key, FrontendDevelopmentConfig)


def setup_logging(app):
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    log_filename = app.config.get('LOG_FILE', 'app.log')
    max_file_size = 10 * 1024 * 1024  # 10 MB
    backup_count = 5  # Keep up to 5 backup files
    
    # Log rotation (choose file rotation based on size or time)
    if app.config.get('ROTATE_LOGS_BY_TIME', False):
        file_handler = TimedRotatingFileHandler(log_filename, when='midnight', backupCount=backup_count)
    else:
        file_handler = RotatingFileHandler(log_filename, maxBytes=max_file_size, backupCount=backup_count)

    if app.config.get('LOG_AS_JSON', False):
        file_handler.setFormatter(jsonlogger.JsonFormatter(log_format))
    else:
        file_handler.setFormatter(logging.Formatter(log_format))
    
    file_handler.setLevel(app.config['LOG_LEVEL'])
    
    # Optionally log to stdout (useful for Docker or cloud environments)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(log_format))
    stream_handler.setLevel(app.config['LOG_LEVEL'])

    # Clear existing handlers and set new ones
    if app.logger.hasHandlers():
        app.logger.handlers.clear()

    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(app.config['LOG_LEVEL'])
    app.logger.propagate = False