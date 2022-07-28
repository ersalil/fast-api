from wsgiref.simple_server import demo_app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import false
from database import SessionLocal
from sqlalchemy.sql import func, desc
import database, datetime
from queries import emb_data
from data import testTableData, testLineData, testBarData, colModel

f = '%Y-%m-%d %H:%M:%S'

app = FastAPI()

origins = ['http://localhost:3000', 'http://127.0.0.1:3000','https://a7d3-182-64-76-131.in.ngrok.io','https://a8ec-182-64-76-131.in.ngrok.io']
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
    result = conn.execute(emb_data(2))
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
            return ls
        for i in ls:
            if i['code'] == dictionary1['code']:
                flag = 1
        if flag == 0:
            ls.append(dictionary1)
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

def roundTime(dt):
    round_mins = 30
    mins = dt.minute - (dt.minute % round_mins)
    return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, mins).strftime("%H:%M")

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
        for v in value:
            # dicTmp = []
            tmp_index= 0
            unique_int = {}
            
            for dic in es:
                # tmp = {}
                if dic['number'] == v:
                    dt = roundTime(dic['added_date'])
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

            ls.append(unique_int)
        
        # for u in unique_int:
        fl = []
        for x in ls:
            dic_time = list(x.items())
            flag = False
            for idx, (dkey,dval) in enumerate(dic_time):
                tmpD = {}
                tmpD['voyage_id'] = dval[1]
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

        # dic_time = list(ls[0].items())
        # for idx, (dkey,dval) in enumerate(dic_time):
        #     tmpD = {}
        #     tmpD['voyage_id'] = dval[1]
        #     tmpD['checkedin_time'] = dkey
        #     if dval[0] == 0:
        #         tmpD['checkedin_couch'] = dval[0]
        #     else:
        #         try:
        #             dval[0] = dval[0] - dic_time[idx+1][1][0]
        #             dic_time[idx][1][0] = dval[0]
        #         except:
        #             pass
        #         tmpD['checkedin_couch'] = dval[0]
        #     fl.append(tmpD)
        


        filter[ship['code']] = fl
    return filter