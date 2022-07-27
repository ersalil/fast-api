from wsgiref.simple_server import demo_app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal
from sqlalchemy.sql import func, desc
import database
from queries import emb_data

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
def shipData():
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
    ships = shipData()
    for dic in es:
        for ship in ships:
            if(dic['code'] == ship['code']):
                dic['name'] = ship['name']
                break
    return es

@app.get('/yash')
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

    
