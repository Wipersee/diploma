from typing import List

from fastapi import APIRouter, HTTPException

from validators.user_schema import CreateUser

from dal import dal_user

user_router = APIRouter()


@user_router.post("/users")
async def create_user(user: CreateUser):
    return await dal_user.create_user(user=user)
