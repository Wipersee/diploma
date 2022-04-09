from uuid import uuid4
from fastapi import FastAPI, UploadFile, File, Depends, Request
from fastapi.encoders import jsonable_encoder
from starlette.middleware.cors import CORSMiddleware
import structlog
from PIL import Image
import io
from validation import verification
from embedding_generator import EmbeddingGenerator
from typing import List
import os
from api.routers import api_router
from config import settings

logger = structlog.get_logger()

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.on_event("startup")
async def startup_event():

    # app.state.model = EmbeddingGenerator(
    #     "face_db_photos", "face_db_embeddings", "face_db_faces"
    # )
    app.state.model = ""


def get_model(request: Request) -> EmbeddingGenerator:
    return request.app.state.model


app.include_router(api_router, prefix=settings.API_V1_STR)

# @app.post("/register")
# async def registration(
#     username: str,
#     photos: List[UploadFile] = File(...),
#     model: EmbeddingGenerator = Depends(get_model),
# ):
#     model.username = username
#     try:
#         os.mkdir(f"face_db_photos/{username}")
#         for photo in photos:
#             file_extension = photo.filename.split(".")[1]
#             photo = await photo.read()
#             Image.open(io.BytesIO(photo)).save(f"face_db_photos/{username}/{str(uuid4())}.{file_extension}")
#     except Exception as e:
#         logger.error(e)
#         return False

#     try:
#         model.setup()
#     except Exception as e:
#         logger.error(e)
#         return False
#     return True


# @app.post("/authz")
# async def authorize(
#     username: str, photo: UploadFile = File(...), model: EmbeddingGenerator = Depends(get_model)
# ):
#     model.username = username
#     data = await photo.read()

#     # Load an image
#     image = Image.open(io.BytesIO(data))

#     return verification(model, image, username)
