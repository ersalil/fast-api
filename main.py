from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from sse_starlette.sse import EventSourceResponse
from fastapi.middleware.cors import CORSMiddleware
from resources.docs import title, description, tags_metadata, logs_stream, home
from api import router, lookup
from config.logging import log, createRequestIdContextvar, getRequestId
from config.setting import get_settings, Settings

app = FastAPI(title=title, description=description, openapi_tags=tags_metadata, docs_url="/api/docs")

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
    createRequestIdContextvar()
    log.debug(f"{request.url} : Request started")

    try:
        response = await call_next(request)

    except Exception as ex:
        log.debug(f"{request.url} : Request failed: {ex}")
        response =  JSONResponse(content={"success": False}, status_code=500)

    finally:
        response.headers["X-Request-ID"] = getRequestId()
        log.debug(f"{request.url} : Request ended")
        return response 


@app.get('/' , summary="ROOT PAGE", description=home)
async def root(settings: Settings = Depends(get_settings)):
    return settings.status.dict()
