from fastapi import FastAPI
import uvicorn

from app.core import config
from app.db.session import SessionLocal
from app.core.auth import get_current_active_user

from service import router 
from fastapi.responses import ORJSONResponse


app = FastAPI(
    title=config.settings.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api", default_response_class=ORJSONResponse
)


from redis.asyncio import Redis
from lazy_load import lazy_func
from fastapi import Request
from redsession import ServerSessionMiddleware
from redsession.backend import RedisBackend

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


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
    