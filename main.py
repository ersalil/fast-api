from multiprocessing import allow_connection_pickling
from wsgiref.simple_server import demo_app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import data

import uvicorn

app = FastAPI()

origins = ['http://localhost:3000','http://127.0.0.1:3000']
app.add_middleware(CORSMiddleware, 
allow_origins = origins,
allow_credentials = True,
allow_methods = ['*'],
allow_headers = ['*']
)

@app.get('/ship/data')
def shipData():
    return data.testTableData

@app.get('/ship/col')
def shipCol():
    return data.colModel

@app.get('/line/data')
def lineData():
    return data.testLineData