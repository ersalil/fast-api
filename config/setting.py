from pydantic import BaseSettings, BaseModel
from db.crud import getLimit
from dotenv import dotenv_values
from functools import lru_cache


@lru_cache()
def get_settings():
    return Settings()

class Status(BaseModel):
    version: str = dotenv_values('.env')['IMAGE_NAME'].split(':')[1]
    port: int = 8000
    health: str = "green"
    name: str = dotenv_values('.env')['CONTAINER_NAME']

class Settings(BaseSettings):
    status = Status()
    
    limit: int = getLimit()

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'