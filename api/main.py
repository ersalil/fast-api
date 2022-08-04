from audioop import reverse
from tabnanny import check
from wsgiref.simple_server import demo_app
from anyio import current_time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import false, null
from database import SessionLocal
from sqlalchemy.sql import func, desc
import database, datetime
from queries import emb_data
from data import colModel

f = '%Y-%m-%d %H:%M:%S'

app = FastAPI()

origins = ['http://localhost:3000', 'http://127.0.0.1:3000']
app.add_middleware(CORSMiddleware,
allow_origins=origins,
allow_credentials=True,
allow_methods=['*'],
allow_headers=['*']
)
db = SessionLocal()

@app.get('/s')
def shipD():
    conn = database.engine.connect()
    result = conn.execute('SELECT ship.name, ship.code FROM ship')
    ls = []
    for r in result:
        ls.append(dict(r))
    return ls

@app.get('/e')
def embSummary():
    conn = database.engine.connect()
    result = conn.execute(emb_data(10))
    ls = []
    for r in result:
        ls.append(dict(r))
    return ls

@app.get('/table/data')
def tableView():
    es = embSummary()
    ls = []
    tempLs = []
    for dictionary1 in es:
        if dictionary1['number'] not in tempLs:
            tempLs.append(dictionary1['number'])
        
    for each in tempLs:
        # each['starting_date'] = current_time()
        flag1 = 0
        minFlag = 99999
        minFlagOnBoard = 99999
        # maxFlag = 0
        temp = null
        tmpDic = {}
        for each1 in es:
            if each1['number'] == each:
                if flag1==0:
                    tmpDic = each1
                    flag1 = 1
                
                ## if we need end date as on board date
                # if maxFlag < each1['checkedin_couch']:
                #     maxFlag = each1['checkedin_couch']
                #     tmpDic['end_date'] = str(datetime.datetime(each1['added_date'].year , each1['added_date'].month , each1['added_date'].day, each1['added_date'].hour, each1['added_date'].minute, each1['added_date'].second)).replace('T', " ")
                #     # flag2 = 1
                # temp = str(datetime.datetime(each1['added_date'].year , each1['added_date'].month , each1['added_date'].day, each1['added_date'].hour, each1['added_date'].minute, each1['added_date'].second)).replace('T', " ")
                
                ## else we need on board date
                if minFlagOnBoard > each1['onboard_couch']:
                    minFlagOnBoard = each1['onboard_couch']
                    tmpDic['end_date'] = str(datetime.datetime(each1['added_date'].year , each1['added_date'].month , each1['added_date'].day, each1['added_date'].hour, each1['added_date'].minute, each1['added_date'].second)).replace('T', " ")

                if minFlag > each1['checkedin_couch']:
                    minFlag = each1['checkedin_couch']
                    tmpDic['start_date'] = str(datetime.datetime(each1['added_date'].year , each1['added_date'].month , each1['added_date'].day, each1['added_date'].hour, each1['added_date'].minute, each1['added_date'].second)).replace('T', " ")
                
        if tmpDic != {}: ls.append(tmpDic)
    return ls
    

@app.get('/ship/col')
def shipCol():
    return colModel

def roundTime(dt):
    round_mins = 30
    mins = dt.minute - (dt.minute % round_mins)
    return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, mins)
    # return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, mins).strftime("%H:%M")


@app.get('/sa')
def salil():
    filter = {}
    ships = shipD()
    es = embSummary()
    for ship in ships:
        value = []
        for dic in es:
            if dic['code'] == ship['code']:
                value.append(dic['number'])
        value = list(set(value))
        ls = []
        # minMaxpership = []
        
        for v in value:
            # dicTmp = []
            tmp_index= 0
            unique_int = {}
            # minMaxList = []
            
            for dic in es:
                # tmp = {}
                if dic['number'] == v:
                    dt = roundTime(dic['added_date'])
                    # minMaxList.append(dt)
                    try:
                        val = dic['checkedin_couch'] - ls[tmp_index-1].values()[0]
                    except:
                        val = dic['checkedin_couch']
                    
                    try:
                        val2 = dic['onboard_couch'] - ls[tmp_index-1].values()[1]
                    except:
                        val2 = dic['onboard_couch']

                    unique_int[dt] = [val,val2,v]
                    tmp_index +=1
            # minMaxpership.append([min(minMaxList),max(minMaxList)])
            ls.append(unique_int)

        fl = []
        for x in ls:
            tmpDate = ''
            tmpDatecount = -1
            dic_time = list(x.items())
            flag = False
            checkDatetime = ''
            for idx, (dkey,dval) in enumerate(dic_time):
                tmpD = {}
                tmpD['voyage_id'] = dval[2]

                dkey = dkey.strftime("%H:%M")
                tmpD['checkedin_time'] = dkey
                tmpD['onboard_time'] = dkey
                tmpD["actual_count"] = dval[0]
                if dval[1] != 0:
                    try:
                        dval[1] = dval[1] - dic_time[idx+1][1][1]
                        dic_time[idx][1][1] = dval[1]
                    except:
                        pass
                    tmpD['onboard_couch'] = dval[1]
                else: tmpD['onboard_couch'] = 0

                if dval[0] != 0:
                    try:
                        dval[0] = dval[0] - dic_time[idx+1][1][0]
                        dic_time[idx][1][0] = dval[0]
                    except:
                        pass
                    tmpD['checkedin_couch'] = dval[0]
                else: tmpD['onboard_couch'] = 0

                if ( dval[0] != 0 or dval[1] != 0 ) or flag:
                    flag = True
                    fl.append(tmpD)

        fl = sorted(fl, key=lambda i: i['checkedin_time'])
        filter[ship['code']] = fl
    return filter

@app.get('/barg/{limit}')
def barg(limit: int):
    ls = salil()
    lst = []
    for each in ls:
        print(each)
        for each1 in ls[each]:
            flag = 0
            avg_checkedin_couch = 0
            avg_onboard_couch = 0
            for eachTime in ls[each]:
                if eachTime['checkedin_time'] == each1['checkedin_time'] and flag < limit:
                    avg_checkedin_couch += eachTime['checkedin_couch']
                    avg_onboard_couch += eachTime['onboard_couch']
                    flag += 1
            avg_checkedin_couch = int(avg_checkedin_couch/limit)
            avg_onboard_couch = int(avg_onboard_couch/limit)
            for eachTime in ls[each]:
                if eachTime['checkedin_time'] == each1['checkedin_time']:
                    if avg_onboard_couch < 0: 
                        avg_onboard_couch = -1*avg_onboard_couch
                    if avg_checkedin_couch < 0:
                        avg_checkedin_couch = -1*avg_checkedin_couch
                    eachTime['avg_checkedin_couch'] = avg_checkedin_couch
                    eachTime['avg_onboard_couch'] = avg_onboard_couch
                    eachTime['ship'] = each 
                    lst.append(eachTime)
    lst = sorted(lst, key=lambda i: i['checkedin_time'])
    return lst
