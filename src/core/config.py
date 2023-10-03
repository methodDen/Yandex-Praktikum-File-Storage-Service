import os

from logging import config as logging_config
from pydantic_settings import BaseSettings

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppSettings(BaseSettings):
    app_title: str = "File Storage"
    project_host: str = "127.0.0.1"
    project_port: int = 8080
    log_database: bool = True
    database_dsn: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


app_settings = AppSettings()