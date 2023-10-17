# from fastapi import APIRouter

# from . import auth, bot, users

# router = APIRouter()

# auth_router = auth.auth_router

# router.include_router(bot.bot_router, 
#                       tags=["bot"],
#                       dependencies=[Depends(get_current_active_user)],
# )

# router.include_router(users.users_router,
#                       tags=["users"],
#                       dependencies=[Depends(get_current_active_user)],
# )