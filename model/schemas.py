# build a schema using pydantic
from datetime import datetime
from pydantic import BaseModel

# define Embark schema and its fields
class Embark(BaseModel):
    voyage_id: str
    added_date: datetime
    oci_completed_core: int
    moci_completed_core: int
    starting_date: datetime
    end_date: datetime

    class Config:
        orm_mode = True

# define Ship schema and its fields
class Ship(BaseModel):
    ship_id = str
    name = str
    code = str

    class Config:
        orm_mode = True

# define Environment schema and its fields
class Environment(BaseModel):
    environment_id = str
    ship_id = str

    class Config:
        orm_mode = True

# define Voyage schema and its fields
class Voyage(BaseModel):
    voyage_id: str
    number: int
    environment_id = str
    embark_date = datetime

    class Config:
        orm_mode = True

# define ApplicationSetting schema and its fields
class ApplicationSetting(BaseModel):
    application_setting_id: str
    value: int

    class Config:
        orm_mode = True
