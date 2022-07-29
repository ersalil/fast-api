# build a schema using pydantic
from datetime import datetime
import uuid
from pydantic import BaseModel

class Embark(BaseModel):
    voyage_id: str
    added_date: datetime
    oci_completed_core: int
    moci_completed_core: int
    starting_date: datetime
    end_date: datetime

    class Config:
        orm_mode = True

class Ship(BaseModel):
    ship_id = str
    name = str
    code = str

    class Config:
        orm_mode = True

class Environment(BaseModel):
    environment_id = str
    ship_id = str

    class Config:
        orm_mode = True

class Voyage(BaseModel):
    voyage_id: str
    number: int
    environment_id = str
    embark_date = datetime

    class Config:
        orm_mode = True