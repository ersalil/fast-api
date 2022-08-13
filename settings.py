from pydantic import BaseSettings
from db.crud import getLimit

class Settings(BaseSettings):
    limit: int = getLimit()
