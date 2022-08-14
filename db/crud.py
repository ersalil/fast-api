from sqlalchemy.orm import Session
from .database import SessionLocal
from model.models import Ship, ApplicationSetting
from fastapi import HTTPException
import json

# message to be displayed when no db connection is available
msg = "Database connection error"

# function that takes db session and returns the names of all ships
def getShip(db: Session):
    try:
        # query the db in ship table and return the names, ids and codes of all ships
        data = db.execute(f"SELECT ship_id, name, code FROM ship")
        if data is None or data == []:
            # if no data is returned, raise an error with status code 404
            raise HTTPException(status_code=404, detail=msg)
        # empty list to store the names, ids and codes of all ships
        result = []
        for row in data:
            # append the data to the result list
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
        # execute the query with limit taken as parameter
        # the get_embark_summary function returns a list of dictionaries, each dictionary contains the data of one voyage corresponding to the time
        data = db.execute(f"SELECT * FROM get_embark_summary({limit})").all()
        if data is None or data == []:
            # if no data is returned, raise an error with status code 404
            raise HTTPException(status_code=404, detail=msg)
        # empty list to store the overview of the most recent voyages
        result = []
        for row in data:
            # append the data to the result list
            result.append(dict(row))
    except Exception as e:
        raise HTTPException(status_code=500, detail=json.dumps({"message":str(msg), "error": str(e)}))
    return result