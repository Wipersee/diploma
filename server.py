from uuid import uuid4
from fastapi import FastAPI, UploadFile, File, Depends, Request
from fastapi.encoders import jsonable_encoder
from starlette.middleware.cors import CORSMiddleware
import structlog
from PIL import Image
import io
from utils.embedding_generator import EmbeddingGenerator
from typing import List
from config.settings import (
    FACE_DB_EMBEDDINGS_PATH,
    FACE_DB_FACES_PATH,
    FACE_DB_PHOTOS_PATH,
)
from api.routers import api_router
from config import settings
import uvicorn

logger = structlog.get_logger()

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.on_event("startup")
async def startup_event():

    # app.state.model = EmbeddingGenerator(
    #     FACE_DB_PHOTOS_PATH, FACE_DB_EMBEDDINGS_PATH, FACE_DB_FACES_PATH
    # )
    app.state.model = ""


def get_model(request: Request) -> EmbeddingGenerator:
    return request.app.state.model


app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
