from fastapi import APIRouter
from api.user_api import user_router
from api.application_api import app_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/auth", tags=["login"])

api_router.include_router(app_router, prefix="/apps", tags=["applications"])
