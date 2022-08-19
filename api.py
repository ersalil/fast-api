from db.crud import getEmbarkationManifest, getEmbarkationBar
from db.database import get_db
from fastapi import Depends, HTTPException, APIRouter
import json
from sqlalchemy.orm import Session
from resources.strings import AVG_VOYAGE_DATA, DATA_NOT_FOUND, INTERNAL_ERROR, DATABASE_ERROR, LIMIT_IS, COLUMN_LOADED, OVERVIEW, VOYAGE_DATA
from resources.docs import table_columns, ship_data, embark_data, avg_voyage_data, data_overview, voyage_data
from config.logging import log
from config.setting import get_settings
from collections import defaultdict

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

router = APIRouter(prefix='/data')
lookup = APIRouter(prefix='/model')

# limit = 10
try:
    limit = get_settings().limit
    log.info(LIMIT_IS, limit)
    if limit == 0 or limit == None:
        limit = 10
        log.warning(DATA_NOT_FOUND, limit)
except Exception as err:
    log.error(DATABASE_ERROR,err)


@lookup.get('/table', tags=['model'], status_code=200, summary="Get table columns", description=table_columns)
async def tableModel():
    try:
        colModel = json.load(open('./resources/colModel.json'))
    except Exception as err:
        log.error(INTERNAL_ERROR,err)
        raise HTTPException(status_code=404, detail=f"Message: {INTERNAL_ERROR}, Traceback: {err}")
    log.debug(COLUMN_LOADED)
    return colModel

# get data for bar graph
@router.get('/voyage', tags=['ship'], status_code=200, summary="Get data for Bar Graph Representation", description=avg_voyage_data)
def linedata(db: Session = Depends(get_db)):
    temp_result = getEmbarkationManifest(db, limit)
    # print(temp_result)
    # return temp_result
    try:
        # # iterate over each ship
        result = defaultdict(list)
        for each in temp_result:
            result[each['ship']].append(each)


        for ship, value in result.items():
            result[ship] = sorted(sorted(value, key=lambda i: i['vnum']), key=lambda i: i['time_int'])
    except Exception as e:
        log.error(INTERNAL_ERROR,err)
        raise HTTPException(status_code=500, detail=f"Message: {INTERNAL_ERROR}, Traceback: {err}")
    finally:
        return result


@router.get('/avg/voyage', tags=['ship'], status_code=200, summary="Get data for Bar Graph Representation", description=avg_voyage_data)
def bardata(db: Session = Depends(get_db)):
    data = getEmbarkationBar(db, limit)
    return data


@router.get('/overview', tags=['ship'], status_code=200, summary="Get data for Bar Graph Representation", description=avg_voyage_data)
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
    except Exception as e:
        log.error(INTERNAL_ERROR,err)
        raise HTTPException(status_code=500, detail=f"Message: {INTERNAL_ERROR}, Traceback: {err}")
    finally:    
        return ls

















        