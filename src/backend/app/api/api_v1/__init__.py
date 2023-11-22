from fastapi import APIRouter, Depends
from app.core.auth import get_current_active_user
from .routers.auth import auth_router
from .routers.bot import bot_router
from .routers.users import users_router
from .services import service_router

# from .routers import router as core_router 
# from .routers import auth_router

v1_router = APIRouter()

# v1_router.include_router(core_router, prefix="/v1")
# v1_router.include_router(auth_router, tags=["auth"])

v1_router.include_router(auth_router, tags=["auth"])

v1_router.include_router(
    users_router,
    prefix="/v1",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
)
# v1_router.include_router(
#     bot_router,
#     prefix="/v1",    
#     tags=["bot"],
#     # dependencies=[Depends(get_current_active_user)],
# )

# v1_router.include_router(
#     embedding_router,
#     prefix="/v1",    
#     tags=["embedding"],
#     # dependencies=[Depends(get_current_active_user)],
# )

v1_router.include_router(service_router, prefix='/v1')


