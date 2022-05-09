from utils.validation import EmbeddingGenerator
from config.settings import (
    FACE_DB_PHOTOS_PATH,
    FACE_DB_EMBEDDINGS_PATH,
    FACE_DB_FACES_PATH,
)

facenet_model = EmbeddingGenerator(
    FACE_DB_PHOTOS_PATH, FACE_DB_EMBEDDINGS_PATH, FACE_DB_FACES_PATH
)
