from multiprocessing import allow_connection_pickling
from tkinter import EXCEPTION
from wsgiref.simple_server import demo_app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import funcfilter
from database import SessionLocal
from schema import Embark, Voyage
from sqlalchemy.sql import func
import data
import model
import uvicorn

app = FastAPI()

origins = ['http://localhost:3000','http://127.0.0.1:3000']
app.add_middleware(CORSMiddleware, 
allow_origins = origins,
allow_credentials = True,
allow_methods = ['*'],
allow_headers = ['*']
)
db = SessionLocal()

@app.get('/ship/data')
def shipData():
    return data.testTableData

@app.get('/ship/col')
def shipCol():
    return data.colModel

@app.get('/line/data')
def lineData():
    return data.testLineData

@app.get('/bar/data')
def barData():
    return data.testBarData

@app.get('/voyage/{vid}', status_code=200)
def get_an_item(vid: str):
    try:
        data = db.query(model.Embark).filter(model.Embark.voyage_id == vid).limit(10).distinct().order_by(model.Embark.added_date.desc()).first()
        return data
    except EXCEPTION as e:
        return e

@app.get('/voyage', status_code=200)
def voyage():
    try:
        data = db.query(model.Embark).distinct(model.Embark.voyage_id).limit(10).all()
        return data
    except EXCEPTION as e:
        return e