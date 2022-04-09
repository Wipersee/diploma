from typing import List

from fastapi import APIRouter, Depends, HTTPException

from validators.user_schema import CreateUser, GetUser

from dal import dal_user, database
from sqlalchemy.orm.session import Session
from starlette.responses import JSONResponse

from starlette.status import HTTP_200_OK, HTTP_409_CONFLICT, HTTP_404_NOT_FOUND

user_router = APIRouter()


@user_router.get("/users")
async def get_all_users(session: Session = Depends(database.get_session)):
    users = await dal_user.get(session=session)
    return [GetUser(
        username = user.username,
        first_name = user.first_name,
        last_name = user.last_name,
        email = user.email,
        active = user.active,
    ) for user in users] 

@user_router.post("/users")
async def create_user(
    user: CreateUser, session: Session = Depends(database.get_session)
):
    if not await dal_user.add(session=session, user=user):
        return JSONResponse(
            status_code=HTTP_409_CONFLICT, content={"info": "User already exists."}
        )
    return JSONResponse(
        status_code=HTTP_200_OK, content={"info": "User created successfully."}
    )
