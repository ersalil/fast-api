from tkinter import E
from sqlalchemy.orm import Session
from .database import SessionLocal
from model.models import Ship, ApplicationSetting
from fastapi import HTTPException
import json
msg = "Database connection error"

def getShip(db: Session):
    try:
        data = db.execute(f"SELECT ship_id, name, code FROM ship")
        if data is None or data == []:
            raise HTTPException(status_code=404, detail=msg)
        result = []
        for row in data:
            result.append(dict(row))
    except Exception as e:
        raise HTTPException(status_code=500, detail=json.dumps({"message":str(msg), "error": str(e)}))
    return result


def getLimit():
    try:
        db = SessionLocal()
        data = db.query(ApplicationSetting.value).filter(ApplicationSetting.application_setting_id == '816063c1-99a2-4cf0-b44e-c6f40397d57c').first()[0]
        if data is None:
            raise HTTPException(status_code=404, detail=msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=json.dumps({"message":str(msg), "error": str(e)}))
    return data


def getEmbarkationSummary(db: Session, limit: int):
    try:
        data = db.execute(f"SELECT * FROM get_embark_summary({limit})").all()
        if data is None or data == []:
            raise HTTPException(status_code=404, detail=msg)
        result = []
        for row in data:
            result.append(dict(row))
    except Exception as e:
        raise HTTPException(status_code=500, detail=json.dumps({"message":str(msg), "error": str(e)}))
    return result