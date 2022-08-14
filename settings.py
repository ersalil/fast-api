from pydantic import BaseSettings
from db.crud import getLimit

# fetch limit from db
class Settings(BaseSettings):
    limit: int = getLimit()
