from app.core.log import configure_logging
from fastapi import FastAPI, Depends
import lazy_load
from starlette.requests import Request
import uvicorn

# from app.api.api_v1.routers.users import users_router
# from app.api.api_v1.routers.bot import bot_router
# from app.api.api_v1.routers.auth import auth_router
from app.core import config
from app.db.session import SessionLocal
from app.core.auth import get_current_active_user
from app.api import router as api
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
  
  
from redsession import ServerSessionMiddleware
from redsession.backend import RedisBackend



app = FastAPI(
    title=config.settings.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api", default_response_class=ORJSONResponse
)


@app.on_event("startup")
async def startup_event():
    configure_logging()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from redis.asyncio import Redis
from lazy_load import lazy_func

@lazy_func
def get_redis_backend():
    REDIS_HOST = config.settings.EMBEDDING_REDIS_HOST
    REDIS_PORT = config.settings.EMBEDDING_REDIS_PORT 
    REDIS_PASSWD = config.settings.EMBEDDING_REDIS_PASSWD
    redis_instance = Redis(host=REDIS_HOST, port=REDIS_PORT,password=REDIS_PASSWD)
    return RedisBackend(redis_instance)

app.add_middleware(
    ServerSessionMiddleware, backend=get_redis_backend(), secret_key=config.settings.SECRET_KEY
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


@app.get("/api/v1")
async def root():
    return {"message": "Hello World"}


# @app.get("/api/v1/task")
# async def example_task():
#     celery_app.send_task("app.tasks.example_task", args=["Hello World"])

#     return {"message": "success"}

@app.get("/health", status_code=200)
async def health_check():
    return {"message": "healthy"}

app.include_router(api)


# Routers
# app.include_router(
#     users_router,
#     prefix="/api/v1",
#     tags=["users"],
#     dependencies=[Depends(get_current_active_user)],
# )
# app.include_router(
#     bot_router,
#     prefix="/api/v1",
#     tags=["bot"],
#     dependencies=[Depends(get_current_active_user)],
# )
# app.include_router(auth_router, prefix="/api", tags=["auth"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
