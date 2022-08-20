# build a schema using pydantic
from datetime import datetime
from pickle import DICT
from typing import Dict, List
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


class EachItemSetVoyage(BaseModel):
    ship: str
    vnum: str
    oci_count: int
    moci_count: int
    diff_checkedin_couch: int
    diff_onboard_couch: int
    time_int: str
    embark_count: int


class EachItemSetAVGVoyage(BaseModel):
    ship: str
    time_int: str
    avg_checkin_count: int
    avg_onboard_count: int


class EachItemSetOverview(BaseModel):
    checkedin_couch: int
    onboard_couch: int
    code: str
    number: str
    oci_completed_core: int
    moci_completed_core: int
    expected_couch: int