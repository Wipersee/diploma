from typing import List

from fastapi import APIRouter, HTTPException

from validators.user_schema import UserCreate

from dal import dal_user

user_router = APIRouter()


@user_router.post("/users")
async def create_user(user: UserCreate):
    db_user = await dal_user.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await dal_user.create_user(user=user)
