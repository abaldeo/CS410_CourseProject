from fastapi import FastAPI
import uvicorn

from app.core import config
from app.db.session import SessionLocal
from app.core.auth import get_current_active_user
from service import router 
from fastapi.responses import ORJSONResponse


app = FastAPI(
    title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api", default_response_class=ORJSONResponse
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
    