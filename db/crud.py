from sqlalchemy.orm import Session
from .database import SessionLocal
from model.models import Ship, ApplicationSetting
from fastapi import HTTPException
import json
msg = "Database connection error"

# function that takes db session and returns the names of all ships
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


# function that fetches the limit (number of records) of the most recent voyages
def getLimit():
    db = SessionLocal()
    return db.query(ApplicationSetting.value).filter(ApplicationSetting.application_setting_id == '816063c1-99a2-4cf0-b44e-c6f40397d57c').first()[0]


# function takes db session and limit and returns the data of the N (N=limit) most recent voyages
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