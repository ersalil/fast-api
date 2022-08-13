from sqlalchemy.orm import Session
from .database import SessionLocal
from model.models import Ship, ApplicationSetting
import json


def getShip(db: Session):
    data = db.execute(f"SELECT ship_id, name, code FROM ship")
    result = []
    for row in data:
        result.append(dict(row))
    return result

def getLimit():
    db = SessionLocal()
    data = db.query(ApplicationSetting.value).filter(ApplicationSetting.application_setting_id == '816063c1-99a2-4cf0-b44e-c6f40397d57c').first()[0]
    return data

def getEmbarkationSummary(db: Session, limit: int):
    data = db.execute(f"SELECT * FROM get_embark_summary({limit})").all()
    result = []
    for row in data:
        result.append(dict(row))
    return result