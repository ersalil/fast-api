
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from resources.docs import title, description, tags_metadata
from api import router, lookup
from db.database import SessionLocal

import logging

app = FastAPI(title=title, description=description, openapi_tags=tags_metadata, docs_url="/api/docs")

# frontend_url in the config file
origins = ['http://localhost:23000', 'http://127.0.0.1:23000', 'http://localhost:3000', 'http://127.0.0.1:3000',"http://app.embarkation-analytics.sreinsights.com","http://app.embarkation-analytics.sreinsights.com:80"]

app.add_middleware(CORSMiddleware,
                    allow_origins=origins,
                    allow_credentials=True,
                    allow_methods=['*'],
                    allow_headers=['*']
                    )

app.include_router(router)
app.include_router(lookup)

@app.get('/')
def root():
    return {"version": "1.2.0",
            "port": "8000",
            "health": "green",
            "name": "sre-embarkation-manifest-backend"
            }

logger = logging.getLogger('emb-mon-log')