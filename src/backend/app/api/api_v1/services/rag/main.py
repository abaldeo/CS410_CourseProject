import uvicorn
from app.core import config
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from service import router

APP = FastAPI(
    title=config.settings.PROJECT_NAME,
    docs_url="/api/docs",
    openapi_url="/api",
    default_response_class=ORJSONResponse,
)

APP.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
