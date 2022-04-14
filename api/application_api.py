from typing import List

from fastapi import APIRouter, Depends

from dal import dal_application, database, dal_user
from sqlalchemy.orm.session import Session
from validators.app_schema import GetAllApps, CreateApp
from starlette.responses import JSONResponse
import structlog
from starlette.status import (
    HTTP_200_OK,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_404_NOT_FOUND,
)

app_router = APIRouter()

logger = structlog.get_logger()


@app_router.get("/")
async def get_all_apps(session: Session = Depends(database.get_session)):
    apps = await dal_application.get_all(session=session)
    return [
        GetAllApps(
            id=app.id, name=app.name, login_url=app.login_url, created_at=app.created_at
        )
        for app in apps
    ]


@app_router.post("/{username}")
async def create_app(
    app: CreateApp, username, session: Session = Depends(database.get_session)
):
    user = await dal_user.get_by_name(session=session, username=username)
    if not user:
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={"message": f"User {username} not found"},
        )
    if not await dal_application.add(session=session, app=app, user_id=user.id):
        return JSONResponse(
            status_code=HTTP_409_CONFLICT, content={"info": "App already exists."}
        )
    return JSONResponse(
        status_code=HTTP_200_OK, content={"info": "App created successfully."}
    )
