# build a schema using pydantic
from datetime import datetime
import uuid
from pydantic import BaseModel

class Embark(BaseModel):
    voyage_id: str
    added_date: datetime
    oci_completed_core: int
    moci_completed_core: int
    checkedin_couch: int
    onboard_couch: int

    class Config:
        orm_mode = True

class Voyage(BaseModel):
    voyage_id: str
    number: int

    class Config:
        orm_mode = True