from wsgiref.simple_server import demo_app
from anyio import current_time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal
from sqlalchemy.sql import func, desc
import database, datetime
from queries import emb_data, emb_data_bar
from data import testTableData, testLineData, testBarData, colModel

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
    result = conn.execute(emb_data(30))
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