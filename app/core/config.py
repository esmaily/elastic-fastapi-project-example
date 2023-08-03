import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    DB_URL: str = Field(..., env='DATABASE_URL')
    BROKER_URL: str = Field(..., env='BROKER_URL')
    ELASTIC_SEARCH_URL: str = Field(..., env='ELASTIC_SEARCH_URL')


settings = Settings()
