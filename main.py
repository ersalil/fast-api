from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from sse_starlette.sse import EventSourceResponse
from fastapi.middleware.cors import CORSMiddleware
from resources.docs import title, description, tags_metadata
from api import router, lookup
from apilogging import log, createRequestIdContextvar, getRequestId

app = FastAPI(title=title, description=description, openapi_tags=tags_metadata, docs_url="/api/docs")

# frontend_url in the config file
origins = ["*"]

app.add_middleware(CORSMiddleware,
                    allow_origins=origins,
                    allow_credentials=True,
                    allow_methods=['*'],
                    allow_headers=['*']
                    )

app.include_router(router)
app.include_router(lookup)

@app.middleware("http")
async def request_middleware(request: Request, call_next):
    createRequestIdContextvar()
    log.logDebug(f"{request.url} : Request started")

    try:
        response = await call_next(request)

    except Exception as ex:
        log.logDebug(f"{request.url} : Request failed: {ex}")
        response =  JSONResponse(content={"success": False}, status_code=500)

    finally:
        response.headers["X-Request-ID"] = getRequestId()
        log.logDebug(f"{request.url} : Request ended")
        return response

@app.get('/')
async def root():
    return {"version": "1.3.0",
            "port": "8000",
            "health": "green",
            "name": "sre-embarkation-manifest-backend"
            }


