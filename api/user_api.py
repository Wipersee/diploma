from typing import List

from fastapi import APIRouter, Depends, UploadFile, Request, File

from validators.user_schema import CreateUser, GetUser

from dal import dal_user, database
from sqlalchemy.orm.session import Session
from starlette.responses import JSONResponse
import structlog
from starlette.status import (
    HTTP_200_OK,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED,
)
import os
import io
from PIL import Image
from utils.embedding_generator import EmbeddingGenerator
from utils.validation import verification
from uuid import uuid4
import shutil

user_router = APIRouter()


def get_model(request: Request) -> EmbeddingGenerator:
    return request.app.state.model


logger = structlog.get_logger()


@user_router.get("/")
async def get_all_users(session: Session = Depends(database.get_session)):
    users = await dal_user.get(session=session)
    return [
        GetUser(
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            active=user.active,
        )
        for user in users
    ]


@user_router.post("/")
async def create_user(
    user: CreateUser, session: Session = Depends(database.get_session)
):
    if not await dal_user.add(session=session, user=user):
        return JSONResponse(
            status_code=HTTP_409_CONFLICT, content={"message": "User already exists."}
        )
    return JSONResponse(
        status_code=HTTP_200_OK, content={"message": "User created successfully."}
    )


@user_router.post("/photos")
async def upload_photo(
    username: str,
    photos: List[UploadFile] = File(...),
    model: EmbeddingGenerator = Depends(get_model),
):
    model.username = username
    dir_name = f"store/face_db_photos/{username}"
    try:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        os.mkdir(dir_name)
        for photo in photos:
            file_extension = photo.filename.split(".")[1]
            photo = await photo.read()
            Image.open(io.BytesIO(photo)).save(
                f"store/face_db_photos/{username}/{str(uuid4())}.{file_extension}"
            )
    except Exception as e:
        logger.error(f"Photo unpacking failed reason: {e}")
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Error while image unpacking"},
        )

    try:
        model.setup()
    except Exception as e:
        logger.error(f"Model training failed reason: {e}")
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Error while model training"},
        )
    return JSONResponse(
        status_code=HTTP_200_OK, content={"message": "Successfully trained model."}
    )


@user_router.post("/authz")
async def authorize(
    username: str,
    photo: UploadFile = File(...),
    model: EmbeddingGenerator = Depends(get_model),
    session: Session = Depends(database.get_session),
):
    if not await dal_user.get_by_name(session=session, username=username):
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={"message": f"User {username} not found"},
        )
    model.username = username
    data = await photo.read()

    # Load an image
    image = Image.open(io.BytesIO(data))

    if not verification(model, image, username):
        return JSONResponse(
            status_code=HTTP_401_UNAUTHORIZED,
            content={"message": f"User {username} not verified"},
        )
    return JSONResponse(
        status_code=HTTP_200_OK, content={"message": f"User {username} verified"}
    )
