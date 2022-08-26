from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from sse_starlette.sse import EventSourceResponse
from fastapi.middleware.cors import CORSMiddleware
from resources.docs import title, description, tags_metadata, introduction
from api import router, lookup
from config.logging import log, createRequestIdContextvar, getRequestId
from config.setting import get_settings, Settings
import time

app = FastAPI(title=title, description=introduction, openapi_tags=tags_metadata, docs_url="/api/docs")

# frontend_url in the config file
origins = ["*"]

# Add CORS middleware
app.add_middleware(CORSMiddleware,
                    allow_origins=origins,
                    allow_credentials=True,
                    allow_methods=['*'],
                    allow_headers=['*']
                    )

# Add API router to the app
app.include_router(router)
app.include_router(lookup)

# home route
@app.middleware("http")
async def request_middleware(request: Request, call_next):
    if request.headers.get('X-Request-ID') is None:
        createRequestIdContextvar()
    else:
        createRequestIdContextvar(id=request.headers.get('X-Request-ID'))
    log.debug(f"{request.url} : Request started")

    try:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
    except Exception as ex:
        log.debug(f"{request.url} : Request failed: {ex}")
        response =  JSONResponse(content={"success": False}, status_code=500)
    finally:
        response.headers["X-Request-ID"] = getRequestId()
        response.headers["X-Process-Time"] = str(process_time)
        log.debug(f"{request.url} : Request ended")
        return response 

@app.get('/' , summary=description["status"]["name"], description=description["status"]['description'])
async def root(settings: Settings = Depends(get_settings)):
    return settings.status.dict()
