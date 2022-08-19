from tabnanny import check
from time import time
from db.crud import getEmbarkationSummary, getShip, getEmbarkationManifest, getEmbarkationBar
from db.database import get_db
from fastapi import Depends, HTTPException, APIRouter
import datetime, json
from sqlalchemy.orm import Session
from resources.strings import AVG_VOYAGE_DATA, DATA_NOT_FOUND, INTERNAL_ERROR, DATABASE_ERROR, LIMIT_IS, COLUMN_LOADED, OVERVIEW, VOYAGE_DATA
from resources.docs import table_columns, ship_data, embark_data, avg_voyage_data, data_overview, voyage_data
from config.logging import log
from config.setting import get_settings
from collections import defaultdict
import pandas as pd

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

@router.get('/ship', tags=['ship'], status_code=200, summary="Get ship data", description=ship_data)
async def shipsData(db: Session = Depends(get_db)):
    try:
        data = getShip(db)
        if data is None or data == []:
            log.error(DATA_NOT_FOUND, data)
            raise HTTPException(status_code=404, detail=DATA_NOT_FOUND)
    except Exception as err:
        log.error(DATABASE_ERROR, err)
        raise HTTPException(status_code=500, detail=json.dumps({"message":str(DATABASE_ERROR), "error": str(err)}))
    return data


# get embarkation summary data
@router.get('/embark', tags=['ship'], status_code=200, summary="Get embarkation summary", description=embark_data)
async def embSummary(db: Session = Depends(get_db)):
    try:
        data = getEmbarkationSummary(db, limit)
        if data is None or data == []:
            log.error(DATA_NOT_FOUND, data)
            raise HTTPException(status_code=404, detail=DATA_NOT_FOUND)
    except Exception as err:
        log.error(DATABASE_ERROR, err)
        raise HTTPException(status_code=500, detail=json.dumps({"message":str(DATABASE_ERROR), "error": str(err)}))
    return data


# # get table data
# @router.get('/overview', tags=['ship'], status_code=200, summary="Get data for Table", description=data_overview)
# def voyOverview(db: Session = Depends(get_db)):
#     es = getEmbarkationSummary(db, limit)
#     try:
#         result = []
#         voy_list = []
#         # get distinct voyage numbers
#         es = list(es)
#         for row in es:
#             if row['number'] not in voy_list:
#                 voy_list.append(row['number'])

#         # find first checkin and onboard date for each voyage
#         for voyage in voy_list:
#             first_entry_check = True
#             min_flag_checkin_count = 99999
#             min_flag_onboard_count = 99999
#             voy_dict = {}

#             # matching all the embark summary data for each voyage
#             for row in es:
#                 if row['number'] == voyage:

#                     # to get latest es data for each voyage and skip the rest
#                     if first_entry_check:
#                         voy_dict = row
#                         first_entry_check = False

#                     # if we need end date as on board date
#                     # if max_flag < row['checkedin_couch']:
#                     #     max_flag = row['checkedin_couch']
#                     #     voy_dict['end_date'] = str(datetime.datetime(row['added_date'].year , row['added_date'].month , row['added_date'].day, row['added_date'].hour, row['added_date'].minute, row['added_date'].second)).replace('T', " ")
#                     #     # flag2 = 1
#                     # temp = str(datetime.datetime(row['added_date'].year , row['added_date'].month , row['added_date'].day, row['added_date'].hour, row['added_date'].minute, row['added_date'].second)).replace('T', " ")

#                     # else we need on board date
#                     # get minimum onboard count and it's respective date
#                     if min_flag_onboard_count > row['onboard_couch']:
#                         min_flag_onboard_count = row['onboard_couch']
#                         voy_dict['end_date'] = str(datetime.datetime(row['added_date'].year, row['added_date'].month, row['added_date'].day,
#                                                                     row['added_date'].hour, row['added_date'].minute, row['added_date'].second)).replace('T', " ")

#                     # get minimum checkin count and it's respective date
#                     if min_flag_checkin_count > row['checkedin_couch']:
#                         min_flag_checkin_count = row['checkedin_couch']
#                         voy_dict['start_date'] = str(datetime.datetime(row['added_date'].year, row['added_date'].month, row['added_date'].day,
#                                                                     row['added_date'].hour, row['added_date'].minute, row['added_date'].second)).replace('T', " ")

#             # ignoring all the empty data
#             if voy_dict != {}:
#                 result.append(voy_dict)
#     except Exception as err:
#         log.error(INTERNAL_ERROR,err)
#         raise HTTPException(status_code=500, detail=f"Message: {INTERNAL_ERROR}, Traceback: {err}")
#     log.info(OVERVIEW, len(result))
#     return result



# # roundup time to it's 30 minutes floor value
# def roundTime(dt):
#     round_mins = 30
#     mins = dt.minute - (dt.minute % round_mins)
#     return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, mins)
#     # return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, mins).strftime("%H:%M")



# # get data for line graph
# @router.get('/voyage', tags=['ship'], status_code=200, summary="Get data for Line Graph Representation", description=voyage_data)
# def voyageData(db: Session = Depends(get_db)):
#     result = {}
#     es = getEmbarkationSummary(db, limit)
#     ships = getShip(db)

#     try:
#         log_data = {}
#         for ship in ships:
#             ship_voy_list = []
#             # get distinct voyage numbers
#             for row in es:
#                 if row['code'] == ship['code']:
#                     ship_voy_list.append(row['number'])
#             ship_voy_list = list(set(ship_voy_list))
#             log_data[ship['code']] = ship_voy_list
#             if ship_voy_list == []:
#                 raise HTTPException(status_code=400, detail="Data can't be found")
#             tmp_result = []

#             for voy_num in ship_voy_list:
#                 tmp_index = 0
#                 voy_data = {}

#                 for row in es:
#                     if row['number'] == voy_num:
#                         dt = roundTime(row['added_date'])
#                         try:
#                             checkedin_count = row['checkedin_couch'] - \
#                                 tmp_result[tmp_index-1].values()[0]
#                         except:
#                             checkedin_count = row['checkedin_couch']

#                         try:
#                             onboard_count = row['onboard_couch'] - \
#                                 tmp_result[tmp_index-1].values()[1]
#                         except:
#                             onboard_count = row['onboard_couch']

#                         voy_data[dt] = [checkedin_count, onboard_count, voy_num]
#                         tmp_index += 1
#                 tmp_result.append(voy_data)
#                 # print(tmp_result)
#                 # print("-----------------------------------------------------")
#             ship_data = []
#             for tmp_voy_data in tmp_result:
#                 dict_time = list(tmp_voy_data.items())
#                 flag = False
#                 for idx, (dkey, dval) in enumerate(dict_time):
#                     dkey = dkey.strftime("%H:%M")

#                     interval_data = {}
#                     interval_data['voyage_id'] = dval[2]
#                     interval_data['checkedin_time'] = dkey
#                     interval_data['onboard_time'] = dkey
#                     interval_data["actual_count"] = dval[0]

#                     if dval[1] != 0:
#                         try:
#                             dval[1] = dval[1] - dict_time[idx+1][1][1]
#                             dict_time[idx][1][1] = dval[1]
#                         except:
#                             pass
#                         interval_data['onboard_couch'] = dval[1]
#                     else:
#                         interval_data['onboard_couch'] = 0

#                     if dval[0] != 0:
#                         try:
#                             dval[0] = dval[0] - dict_time[idx+1][1][0]
#                             dict_time[idx][1][0] = dval[0]
#                         except:
#                             pass
#                         interval_data['checkedin_couch'] = dval[0]
#                     else:
#                         interval_data['checkedin_couch'] = 0

#                     if (dval[0] != 0 or dval[1] != 0) or flag:
#                         flag = True
#                         ship_data.append(interval_data)

#             ship_data = sorted(ship_data, key=lambda i: i['voyage_id'])

#             ship_data = sorted(ship_data, key=lambda i: i['checkedin_time'])
#             result[ship['code']] = ship_data
#     except Exception as err:
#         log.error(INTERNAL_ERROR,err)
#         raise HTTPException(status_code=500, detail=f"Message: {INTERNAL_ERROR}, Traceback: {err}")
#     log.info(VOYAGE_DATA, log_data)
#     return result



# # get data for bar graph
# @router.get('/avg/voyage', tags=['ship'], status_code=200, summary="Get data for Bar Graph Representation", description=avg_voyage_data)
# def avgVoyageData(db: Session = Depends(get_db)):
#     temp_result = voyageData(db)
#     try:
#         result = []
#         # iterate over each ship
#         for each_dict in temp_result:
#             # iterate over each voyage
#             for row in temp_result[each_dict]:
#                 count = 0
#                 avg_checkedin_couch = 0
#                 avg_onboard_couch = 0
#                 for each_time in temp_result[each_dict]:
#                     if each_time['checkedin_time'] == row['checkedin_time'] and count < limit:
#                         avg_checkedin_couch += each_time['checkedin_couch']
#                         avg_onboard_couch += each_time['onboard_couch']
#                         count += 1
#                 avg_checkedin_couch = int(avg_checkedin_couch/limit)
#                 avg_onboard_couch = int(avg_onboard_couch/limit)
#                 for each_time in temp_result[each_dict]:
#                     if each_time['checkedin_time'] == row['checkedin_time']:
#                         if avg_onboard_couch < 0:
#                             avg_onboard_couch = -1*avg_onboard_couch
#                         if avg_checkedin_couch < 0:
#                             avg_checkedin_couch = -1*avg_checkedin_couch
#                         each_time['avg_checkedin_couch'] = avg_checkedin_couch
#                         each_time['avg_onboard_couch'] = avg_onboard_couch
#                         each_time['ship'] = each_dict
#                         result.append(each_time)
#         result = sorted(result, key=lambda i: i['checkedin_time'])
#     except Exception as err:
#         log.error(INTERNAL_ERROR,err)
#         raise HTTPException(status_code=500, detail=f"Message: {INTERNAL_ERROR}, Traceback: {err}")
#     log.info(AVG_VOYAGE_DATA, len(result))
#     return result





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
    # print(temp_result)
    # return temp_result
    # try:
    #     data.groupby(['ship', 'time_int']).agg({'diff_checkedin_couch':'mean'})
    #     data = data.to_dict('records')
    #     data = sorted(data, key=lambda i: i['time_int'])
    #     print(data)
    # except Exception as e:
    #     log.error(INTERNAL_ERROR,err)
    #     raise HTTPException(status_code=500, detail=f"Message: {INTERNAL_ERROR}, Traceback: {err}")
    # finally:    
    #     return data

@router.get('/overview', tags=['ship'], status_code=200, summary="Get data for Bar Graph Representation", description=avg_voyage_data)
def tabledata(db: Session = Depends(get_db)):
    data = getEmbarkationManifest(db, limit)

    # print(temp_result)
    # return temp_result
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

















        