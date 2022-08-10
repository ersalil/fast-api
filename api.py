from db.sql import app_setting, ship_data, embarkData
from db.database import executeSQL
from fastapi import Depends, HTTPException
import datetime, json

from fastapi import APIRouter

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

router = APIRouter(prefix='/data')
lookup = APIRouter(prefix='/model')

limit = 10

def appSetting():
    global limit 
    limit = int(executeSQL(app_setting)[0]['value'])

appSetting()

@lookup.get('/table', tags=['model'])
def tableModel():
    colModel = json.load(open('./resources/colModel.json'))
    return colModel

@router.get('/ship', tags=['ship'])
def shipsData():
    data = executeSQL(ship_data)
    print(data)
    if data is None:
        raise HTTPException(status_code=404, detail='Ship data not found')
    return data


# get embarkation summary data
@router.get('/embark', tags=['ship'])
def embSummary():
    global limit
    if limit == None:
        raise HTTPException(status_code=500, detail='Application setting not found')
    data = executeSQL(embarkData(limit))
    if data is None:
        raise HTTPException(status_code=404, detail='Embarkation data not found')
    return data
    

# get table data
@router.get('/overview', tags=['ship'])
def voyOverview(es=Depends(embSummary)):
    if es == [] or es == None:
        raise HTTPException(status_code=400, detail="Data can't be found")
    result = []
    voy_list = []
    # get distinct voyage numbers
    for row in es:
        if row['number'] not in voy_list:
            voy_list.append(row['number'])

    # find first checkin and onboard date for each voyage
    for voyage in voy_list:
        first_entry_check = True
        min_flag_checkin_count = 99999
        min_flag_onboard_count = 99999
        voy_dict = {}

        # matching all the embark summary data for each voyage
        for row in es:
            if row['number'] == voyage:

                # to get latest es data for each voyage and skip the rest
                if first_entry_check:
                    voy_dict = row
                    first_entry_check = False

                # if we need end date as on board date
                # if max_flag < row['checkedin_couch']:
                #     max_flag = row['checkedin_couch']
                #     voy_dict['end_date'] = str(datetime.datetime(row['added_date'].year , row['added_date'].month , row['added_date'].day, row['added_date'].hour, row['added_date'].minute, row['added_date'].second)).replace('T', " ")
                #     # flag2 = 1
                # temp = str(datetime.datetime(row['added_date'].year , row['added_date'].month , row['added_date'].day, row['added_date'].hour, row['added_date'].minute, row['added_date'].second)).replace('T', " ")

                # else we need on board date
                # get minimum onboard count and it's respective date
                if min_flag_onboard_count > row['onboard_couch']:
                    min_flag_onboard_count = row['onboard_couch']
                    voy_dict['end_date'] = str(datetime.datetime(row['added_date'].year, row['added_date'].month, row['added_date'].day,
                                                                 row['added_date'].hour, row['added_date'].minute, row['added_date'].second)).replace('T', " ")

                # get minimum checkin count and it's respective date
                if min_flag_checkin_count > row['checkedin_couch']:
                    min_flag_checkin_count = row['checkedin_couch']
                    voy_dict['start_date'] = str(datetime.datetime(row['added_date'].year, row['added_date'].month, row['added_date'].day,
                                                                   row['added_date'].hour, row['added_date'].minute, row['added_date'].second)).replace('T', " ")

        # ignoring all the empty data
        if voy_dict != {}:
            result.append(voy_dict)
        if result == []:
            raise HTTPException(status_code=400, detail="Data can't be found")
    return result



# roundup time to it's 30 minutes floor value
def roundTime(dt):
    round_mins = 30
    mins = dt.minute - (dt.minute % round_mins)
    return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, mins)
    # return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, mins).strftime("%H:%M")



# get data for line graph
@router.get('/voyage', tags=['ship'])
def voyageData():
    result = {}
    es = embSummary()
    ships = shipsData()
    if ships == [] or ships == None:
        raise HTTPException(status_code=400, detail="Data can't be found")
    if es == [] or es == None:
        raise HTTPException(status_code=400, detail="Data can't be found")
    for ship in ships:
        ship_voy_list = []
        for row in es:
            if row['code'] == ship['code']:
                ship_voy_list.append(row['number'])
        ship_voy_list = list(set(ship_voy_list))
        if ship_voy_list == []:
            raise HTTPException(status_code=400, detail="Data can't be found")
        tmp_result = []

        for voy_num in ship_voy_list:
            tmp_index = 0
            voy_data = {}

            for row in es:
                if row['number'] == voy_num:
                    dt = roundTime(row['added_date'])
                    try:
                        checkedin_count = row['checkedin_couch'] - \
                            tmp_result[tmp_index-1].values()[0]
                    except:
                        checkedin_count = row['checkedin_couch']

                    try:
                        onboard_count = row['onboard_couch'] - \
                            tmp_result[tmp_index-1].values()[1]
                    except:
                        onboard_count = row['onboard_couch']

                    voy_data[dt] = [checkedin_count, onboard_count, voy_num]
                    tmp_index += 1
            tmp_result.append(voy_data)
            # print(tmp_result)
            # print("-----------------------------------------------------")
        ship_data = []
        for tmp_voy_data in tmp_result:
            dict_time = list(tmp_voy_data.items())
            flag = False
            for idx, (dkey, dval) in enumerate(dict_time):
                dkey = dkey.strftime("%H:%M")

                interval_data = {}
                interval_data['voyage_id'] = dval[2]
                interval_data['checkedin_time'] = dkey
                interval_data['onboard_time'] = dkey
                interval_data["actual_count"] = dval[0]

                if dval[1] != 0:
                    try:
                        dval[1] = dval[1] - dict_time[idx+1][1][1]
                        dict_time[idx][1][1] = dval[1]
                    except:
                        pass
                    interval_data['onboard_couch'] = dval[1]
                else:
                    interval_data['onboard_couch'] = 0

                if dval[0] != 0:
                    try:
                        dval[0] = dval[0] - dict_time[idx+1][1][0]
                        dict_time[idx][1][0] = dval[0]
                    except:
                        pass
                    interval_data['checkedin_couch'] = dval[0]
                else:
                    interval_data['checkedin_couch'] = 0

                if (dval[0] != 0 or dval[1] != 0) or flag:
                    flag = True
                    ship_data.append(interval_data)

        ship_data = sorted(ship_data, key=lambda i: i['checkedin_time'])
        result[ship['code']] = ship_data
    return result



# get data for bar graph
@router.get('/avg/voyage', tags=['ship'])
def avgVoyageData():
    global limit
    temp_result = voyageData()
    if limit == None:
        raise HTTPException(status_code=500, detail='Application setting not found')
    # store result of line graph in a dictionary and then sort it by date 
    if temp_result == [] or temp_result == None:
        raise HTTPException(status_code=400, detail="Data can't be found")
    result = []
    # iterate over each ship
    for each_dict in temp_result:
        # iterate over each voyage
        for row in temp_result[each_dict]:
            count = 0
            avg_checkedin_couch = 0
            avg_onboard_couch = 0
            for each_time in temp_result[each_dict]:
                if each_time['checkedin_time'] == row['checkedin_time'] and count < limit:
                    avg_checkedin_couch += each_time['checkedin_couch']
                    avg_onboard_couch += each_time['onboard_couch']
                    count += 1
            avg_checkedin_couch = int(avg_checkedin_couch/limit)
            avg_onboard_couch = int(avg_onboard_couch/limit)
            for each_time in temp_result[each_dict]:
                if each_time['checkedin_time'] == row['checkedin_time']:
                    if avg_onboard_couch < 0:
                        avg_onboard_couch = -1*avg_onboard_couch
                    if avg_checkedin_couch < 0:
                        avg_checkedin_couch = -1*avg_checkedin_couch
                    each_time['avg_checkedin_couch'] = avg_checkedin_couch
                    each_time['avg_onboard_couch'] = avg_onboard_couch
                    each_time['ship'] = each_dict
                    result.append(each_time)
    result = sorted(result, key=lambda i: i['checkedin_time'])
    return result
