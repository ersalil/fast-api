from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal
import database
import datetime
from queries import emb_data
from data import colModel

f = '%Y-%m-%d %H:%M:%S'

app = FastAPI()

origins = ['http://localhost:3000', 'http://127.0.0.1:3000',
           'https://d854-182-73-51-26.in.ngrok.io', 'https://28e8-182-73-51-26.in.ngrok.io']
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentiaresult=True,
                   allow_methods=['*'],
                   allow_headers=['*']
                   )
db = SessionLocal()


@app.get('/ship')
def shipData():
    conn = database.engine.connect()
    result = conn.execute('SELECT ship.name, ship.code FROM ship')
    result = []
    for row in result:
        result.append(dict(row))
    return result


@app.get('/embark/data')
def embSummary():
    conn = database.engine.connect()
    result = conn.execute(emb_data(10))
    result = []
    for row in result:
        result.append(dict(row))
    return result


@app.get('/table/data')
def tableView():
    es = embSummary()
    result = []
    voy_list = []
    for row in es:
        if row['number'] not in voy_list:
            voy_list.append(row['number'])

    for voyage in voy_list:
        first_entry_check = 0
        min_flag_checkin_count = 99999
        min_flag_onboard_count = 99999
        voy_dict = {}
        for row in es:
            if row['number'] == voyage:
                if first_entry_check == 0:
                    voy_dict = row
                    first_entry_check = 1

                # if we need end date as on board date
                # if max_flag < row['checkedin_couch']:
                #     max_flag = row['checkedin_couch']
                #     voy_dict['end_date'] = str(datetime.datetime(row['added_date'].year , row['added_date'].month , row['added_date'].day, row['added_date'].hour, row['added_date'].minute, row['added_date'].second)).replace('T', " ")
                #     # flag2 = 1
                # temp = str(datetime.datetime(row['added_date'].year , row['added_date'].month , row['added_date'].day, row['added_date'].hour, row['added_date'].minute, row['added_date'].second)).replace('T', " ")

                # else we need on board date
                if min_flag_onboard_count > row['onboard_couch']:
                    min_flag_onboard_count = row['onboard_couch']
                    voy_dict['end_date'] = str(datetime.datetime(row['added_date'].year, row['added_date'].month, row['added_date'].day,
                                                                 row['added_date'].hour, row['added_date'].minute, row['added_date'].second)).replace('T', " ")

                if min_flag_checkin_count > row['checkedin_couch']:
                    min_flag_checkin_count = row['checkedin_couch']
                    voy_dict['start_date'] = str(datetime.datetime(row['added_date'].year, row['added_date'].month, row['added_date'].day,
                                                                   row['added_date'].hour, row['added_date'].minute, row['added_date'].second)).replace('T', " ")

        if voy_dict != {}:
            result.append(voy_dict)
    return result


@app.get('/ship/col')
def shipCol():
    return colModel


def roundTime(dt):
    round_mins = 30
    mins = dt.minute - (dt.minute % round_mins)
    return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, mins)
    # return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, mins).strftime("%H:%M")

@app.get('/lineGraph')
def lineGraph():
    result = {}
    ships = ship_data()
    es = embSummary()
    for ship in ships:
        ship_voy_list = []
        for row in es:
            if row['code'] == ship['code']:
                ship_voy_list.append(row['number'])
        ship_voy_list = list(set(ship_voy_list))
        tmp_result = []

        for voy_num in ship_voy_list:
            tmp_index = 0
            voy_data = {}

            for row in es:
                if row['number'] == voy_num:
                    dt = roundTime(row['added_date'])
                    try:
                        chck_cnt = row['checkedin_couch'] - \
                            tmp_result[tmp_index-1].values()[0]
                    except:
                        chck_cnt = row['checkedin_couch']

                    try:
                        onBrdCnt = row['onboard_couch'] - \
                            tmp_result[tmp_index-1].values()[1]
                    except:
                        onBrdCnt = row['onboard_couch']

                    voy_data[dt] = [chck_cnt, onBrdCnt, voy_num]
                    tmp_index += 1
            tmp_result.append(voy_data)

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
                    interval_data['onboard_couch'] = 0

                if (dval[0] != 0 or dval[1] != 0) or flag:
                    flag = True
                    ship_data.append(interval_data)

        ship_data = sorted(ship_data, key=lambda i: i['checkedin_time'])
        result[ship['code']] = ship_data
    return result


@app.get('/barg/{limit}')
def barg(limit: int):
    temp_result = lineGraph()
    result = []
    for each_dict in temp_result:
        print(each_dict)
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
