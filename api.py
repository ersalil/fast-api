from db.crud import getEmbarkationManifest, getEmbarkationBar
from db.database import get_db
from fastapi import Depends, HTTPException, APIRouter
import json
from sqlalchemy.orm import Session
from resources.strings import AVG_VOYAGE_DATA, DATA_NOT_FOUND, INTERNAL_ERROR, DATABASE_ERROR, LIMIT_IS, COLUMN_LOADED, OVERVIEW, VOYAGE_DATA
from resources.docs import description
from config.logging import log
from config.setting import get_settings
from collections import defaultdict
from model.schemas import EachItemSetAVGVoyage, EachItemSetOverview, EachItemSetVoyage
from typing import Dict, List

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

router = APIRouter(prefix='/data')
lookup = APIRouter(prefix='/model')

# limit: N most recent voyages of each ship
try:
    limit = get_settings().limit
    log.info(LIMIT_IS, limit)
    if limit == 0 or limit == None:
        limit = 10
        log.warning(DATA_NOT_FOUND, limit)
except Exception as err:
    log.error(DATABASE_ERROR,err)

# get column names from table
@lookup.get('/table', tags=['Lookup Data'], status_code=200, summary=description['table_keys']['name'], description=description['table_keys']['description'])
async def tableModel():
    try:
        colModel = json.load(open('./resources/colModel.json'))
    except Exception as err:
        log.error(INTERNAL_ERROR,err)
        raise HTTPException(status_code=404, detail=f"Message: {INTERNAL_ERROR}, Traceback: {err}")
    log.debug(COLUMN_LOADED)
    return colModel


# getting all checkedin and onboard counts for n voyages for each ships
@router.get('/voyage', response_model=Dict[str, List[EachItemSetVoyage]], tags=['Master Data'], status_code=200, summary=description['voyage']['name'], description=description['voyage']['description'])
def linedata(db: Session = Depends(get_db)):
    temp_result = getEmbarkationManifest(db, limit)
    try:
        # # iterate over each ship
        result = defaultdict(list)
        for each in temp_result:
            result[each['ship']].append(each)
        for ship, value in result.items():
            result[ship] = sorted(sorted(value, key=lambda i: i['vnum']), key=lambda i: i['time_int'])
    except Exception as err:
        log.error(INTERNAL_ERROR,err)
        raise HTTPException(status_code=500, detail=f"Message: {INTERNAL_ERROR}, Traceback: {err}")
    finally:
        return result

# getting the Average Checkedin and Onboard Count for all voyages for a ship
# Data like: {'ship': 'ship_name','time_int': 'time', 'avg_checkin_count': avg_checkin, 'avg_onboard_count': avg_onboard}
@router.get('/avg/voyage', response_model=List[EachItemSetAVGVoyage], tags=['Master Data'], status_code=200, summary=description['avg_voyage']['name'], description=description['avg_voyage']['description'])
def bardata(db: Session = Depends(get_db)):
    data = getEmbarkationBar(db, limit)
    try:        
        result = sorted(data, key=lambda i: i['time_int'])    
    except Exception as err:
        log.error(INTERNAL_ERROR,err)
        raise HTTPException(status_code=500, detail=f"Message: {INTERNAL_ERROR}, Traceback: {err}")
    finally:
        return result

# getting the overview data or brief summary of each voyage
# Data like: Ship Code, Voyage Number, Embarkation Count,
#            OCI Count, MOCI Count, Checkedin Time and OnBoard Time
@router.get('/overview', response_model=List[EachItemSetOverview], tags=['Master Data'], status_code=200, summary=description['overview']['name'], description=description['overview']['description'])
def tabledata(db: Session = Depends(get_db)):
    data = getEmbarkationManifest(db, limit)
    try:
        ls = []
        chck = []
        for each in data:
            if each['vnum'] not in chck: 
                res = {}
                flag_checkedin = True
                flag_onboard = True
                final_flag = True
            chck.append(each['vnum'])
            if each['diff_checkedin_couch'] != 0 and flag_checkedin:
                res['checkedin_time'] = each['time_int']
                flag_checkedin = False
            if each['diff_onboard_couch'] != 0 and flag_onboard:
                res['onboard_time'] = each['time_int']
                flag_onboard = False
            if flag_onboard is False and flag_onboard is False and final_flag:
                final_flag = False
                res['code'] = each['ship']
                res['number'] = each['vnum'] 
                res['oci_completed_core'] = each['oci_count']
                res['moci_completed_core'] = each['moci_count']
                res['expected_couch'] = each['embark_count']
                ls.append(res)
    except Exception as err:
        log.error(INTERNAL_ERROR,err)
        raise HTTPException(status_code=500, detail=f"Message: {INTERNAL_ERROR}, Traceback: {err}")
    finally:    
        return ls

















        