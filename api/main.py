from tabnanny import check
from wsgiref.simple_server import demo_app
from anyio import current_time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import false
from database import SessionLocal
from sqlalchemy.sql import func, desc
import database, datetime
from queries import emb_data, emb_data_bar
from data import testTableData, testLineData, testBarData, colModel
from datetimerange import DateTimeRange

f = '%Y-%m-%d %H:%M:%S'

app = FastAPI()

origins = ['http://localhost:3000', 'http://127.0.0.1:3000','https://d854-182-73-51-26.in.ngrok.io','https://28e8-182-73-51-26.in.ngrok.io']
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

@app.get('/')
def main():
    es = embSummary()
    ships = shipD()
    for dic in es:
        for ship in ships:
            if(dic['code'] == ship['code']):
                dic['name'] = ship['name']
                break
    return es

@app.get('/table/data')
def tableView():
    es = embSummary()
    ls = []
    for dictionary1 in es:
        flag = 0
        if len(ls) == 5:
            break
        for i in ls:
            if i['code'] == dictionary1['code']:
                flag = 1
        if flag == 0:
            ls.append(dictionary1)
        for each in ls:
            # each['starting_date'] = current_time()
            flag1 = 0
            flag2 = 0
            inti = each['checkedin_couch']
            for each1 in es:
                if each1['voyage_id'] == each['voyage_id'] and each1['checkedin_couch'] < inti and flag1 == 0:
                    each['end_date'] = str(datetime.datetime(each1['added_date'].year , each1['added_date'].month , each1['added_date'].day, each1['added_date'].hour, each1['added_date'].minute, each1['added_date'].second)).replace('T', " ")
                    flag1 = 1
            # // reverse loop to find the latest date
            for each2 in es:
                if each2['voyage_id'] == each['voyage_id'] and each2['checkedin_couch'] == 0 < inti and flag2 == 0:
                    each['starting_date'] = str(datetime.datetime(each2['added_date'].year , each2['added_date'].month , each2['added_date'].day, each2['added_date'].hour, each2['added_date'].minute, each2['added_date'].second)).replace('T', " ")
                    flag2 = 1
    return ls
    

@app.get('/ship/data')
def shipData():
    return testTableData


@app.get('/ship/col')
def shipCol():
    return colModel


@app.get('/line/data')
def lineData():
    return testLineData


@app.get('/bar/data')
def barData():
    return testBarData


# @app.get('/bar/data/{limit}')
# def barData(limit):
#     return emb_data_bar(limit)
def roundTime(dt):
    round_mins = 30
    mins = dt.minute - (dt.minute % round_mins)
    return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, mins)
    # return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, mins).strftime("%H:%M")

# @app.get('/voy')
# def voyage():
#     conn = database.engine.connect()
#     result = conn.execute(voyage_data())
#     ls = []
#     for r in result:
#         ls.append(dict(r))
#     return ls

# @app.get('/t')
# def st():
#     vy = voyage()
#     mainD = []
#     for x in vy:   
#         conn = database.engine.connect()
#         tmpR = conn.execute(a(x['vid'], x['edate'],x['ddate']))
#         mainD.append(tmpR)
#     return mainD








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
        minMaxpership = []
        
        for v in value:
            # dicTmp = []
            tmp_index= 0
            unique_int = {}
            minMaxList = []
            
            for dic in es:
                # tmp = {}
                if dic['number'] == v:
                    dt = roundTime(dic['added_date'])
                    minMaxList.append(dt)
                    # tmp['voyage_id'] = v

                    # try:
                    #     tmp['checkedin'] = dic['checkedin_couch'] - dicTmp[tmp_index]['checkedin']
                    # except:
                    #     tmp['checkedin'] = dic['checkedin_couch']

                    # tmp['datetime'] = dt
                    
                    try:
                        val = dic['checkedin_couch'] - ls[tmp_index-1].values()[0]
                    except:
                        val = dic['checkedin_couch']

                    unique_int[dt] = [val,v]

                    
                    # tmp['entry_time'] = dic['added_date']

                    # dicTmp.append(tmp)
                    tmp_index +=1
            minMaxpership.append([min(minMaxList),max(minMaxList)])
            ls.append(unique_int)
        
        # for u in unique_int:
        # fl = []
        # for x, y in zip(ls,minMaxpership):
        #     dic_time = list(x.items())
        #     dateTimeRange = DateTimeRange(y[0], y[1])
        #     for r in dateTimeRange.range(datetime.timedelta(minutes=30)):
        #         for idx, (dkey,dval) in enumerate(dic_time):
                    
        #             tmpD = {}
        #             tmpD['voyage_id'] = dval[1]
        #             if dkey == r:
                        
        #                 dkey = dkey.strftime("%H:%M")
        #                 tmpD['checkedin_time'] = dkey
        #                 tmpD['onboard_time'] = dkey
        #                 tmpD["actual_count"] = dval[0]

        #                 if dval[0] != 0:
        #                     try:
        #                         dval[0] = dval[0] - dic_time[idx+1][1][0]
        #                         dic_time[idx][1][0] = dval[0]
        #                     except:
        #                         pass
        #                     tmpD['checkedin_couch'] = dval[0]
        #                     tmpD['onboard_couch'] = dval[0]
        #                     if dval[0] != 0:
        #                         flag = True
        #                         fl.append(tmpD)
                    
        # fl = sorted(fl, key=lambda i: i['checkedin_time'])
        
    #     filter[ship['code']] = fl
    # return filter




        fl = []
        for x in ls:
            tmpDate = ''
            tmpDatecount = -1
            dic_time = list(x.items())
            flag = False
            checkDatetime = ''
            for idx, (dkey,dval) in enumerate(dic_time):
                if checkDatetime == '': checkDatetime = dkey.strftime("%H:%M")
                if tmpDate != dkey.date():
                    tmpDate = dkey.date()
                    tmpDatecount+=1
                    print("upadte hua in ", tmpDatecount, '/t',dkey.date())
                print(":::::    ", tmpDatecount, '/t',dkey.date(), "    :::::")
                tmpD = {}
                tmpD['voyage_id'] = dval[1]

                dkey = dkey.strftime("%H:%M")
                if checkDatetime > dkey:
                    print('warning here', dval[1])
                checkDatetime = dkey

                if tmpDatecount != 0:
                    tmpD['checkedin_time'] = str(tmpDatecount) + '+' + str(dkey)
                    print(tmpD['checkedin_time'])
                else:
                    tmpD['checkedin_time'] = dkey

                tmpD['onboard_time'] = dkey
                tmpD["actual_count"] = dval[0]
                if dval[0] != 0:
                    try:
                        dval[0] = dval[0] - dic_time[idx+1][1][0]
                        dic_time[idx][1][0] = dval[0]
                    except:
                        pass
                    tmpD['checkedin_couch'] = dval[0]
                    tmpD['onboard_couch'] = dval[0]
                    if dval[0] != 0 or flag:
                        flag = True
                        fl.append(tmpD)

        fl = sorted(fl, key=lambda i: i['checkedin_time'])
        filter[ship['code']] = fl
    return filter
