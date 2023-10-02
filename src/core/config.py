import os

from logging import config as logging_config
from pydantic_settings import BaseSettings

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppSettings(BaseSettings):
    pass

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


app_settings = AppSettings()