import os
from logging import config as logging_config

from pydantic import BaseSettings
from .logger import LOGGING

logging_config.dictConfig(LOGGING)


class DatabaseDSN(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str


class RedisDSN(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int


# class Stripe(BaseSettings):
#     STRIPE__API_KEY: str
#     STRIPE__WEBHOOK_SECRET: str
#     STRIPE__BALANCE_PROD_ID: str


class Project(BaseSettings):
    PROJECT_NAME: str
    PROJECT_DOMAIN: str
    PROJECT_PORT: int
    DEBUG: bool


# class Sentry(BaseSettings):
#     SENTRY_ENABLED: bool = False
#     SENTRY_DSN: str = ''


class Settings(BaseSettings):
    DB: DatabaseDSN = DatabaseDSN()
    REDIS: RedisDSN = RedisDSN()
    # STRIPE: Stripe = Stripe()
    PROJECT: Project = Project()
    # SENTRY: Sentry = Sentry()

    SQLALCHEMY_DATABASE_URL = \
        f"postgresql+asyncpg://{DB.POSTGRES_USER}:{DB.POSTGRES_PASSWORD}@{DB.POSTGRES_HOST}:{DB.POSTGRES_PORT}/{DB.POSTGRES_DB}"
    # PROJECT_URL = f"http://{PROJECT.PROJECT_DOMAIN}:{PROJECT.PROJECT_PORT}"

    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ORM_ECHO: bool = True if PROJECT.DEBUG else False


SETTINGS = Settings()
