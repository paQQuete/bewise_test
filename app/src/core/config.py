import enum
import os
from logging import config as logging_config

from dotenv import load_dotenv
from pydantic import BaseSettings
from .logger import LOGGING

logging_config.dictConfig(LOGGING)

DEBUG = True
if DEBUG:
    load_dotenv()


class Base(BaseSettings):
    class Config:
        env_file = '.env'


class DatabaseDSN(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str


class Project(BaseSettings):
    PROJECT_NAME: str
    PROJECT_DOMAIN: str
    PROJECT_PORT: int
    DEBUG: bool
    QUESTIONS_URI: str


class ApiTypesURI(enum.Enum):
    RANDOM = 'random/'
    CLUES = 'clues/'
    FINAL = 'final/'
    CATEGORIES = 'categories/'
    CATEGORY = 'category/'


class Settings(BaseSettings):
    DB: DatabaseDSN = DatabaseDSN()
    PROJECT: Project = Project()

    SQLALCHEMY_DATABASE_URL = \
        f"postgresql+asyncpg://{DB.POSTGRES_USER}:{DB.POSTGRES_PASSWORD}@{DB.POSTGRES_HOST}:{DB.POSTGRES_PORT}/{DB.POSTGRES_DB}"
    SQLALCHEMY_DATABASE_URL_SYNC = \
        f"postgresql://{DB.POSTGRES_USER}:{DB.POSTGRES_PASSWORD}@{DB.POSTGRES_HOST}:{DB.POSTGRES_PORT}/{DB.POSTGRES_DB}"

    PROJECT_URL = f"http://{PROJECT.PROJECT_DOMAIN}:{PROJECT.PROJECT_PORT}"
    Q_API = f"https://{PROJECT.QUESTIONS_URI}"
    ALLOWED_EXTENSIONS = {"wav", }
    ALLOWED_MIMETYPES = {"audio/x-wav", }

    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MP3_CONTENT_PATH: str = f"media/mp3"
    ORM_ECHO: bool = True if PROJECT.DEBUG else False


SETTINGS = Settings()
