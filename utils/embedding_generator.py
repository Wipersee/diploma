import os
from os.path import isdir
from PIL import Image
from matplotlib import pyplot
from numpy import savez_compressed, asarray, load, expand_dims
from mtcnn.mtcnn import MTCNN
from tensorflow.keras.models import load_model
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer
from sklearn.svm import SVC
from random import choice
from matplotlib import pyplot
import logging
import structlog

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(),
        structlog.dev.ConsoleRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=False,
)
logger = structlog.get_logger()


class EmbeddingGenerator:
    def __init__(
        self, dir_train, dir_embeddings: str, dir_faces: str, username: str = None
    ) -> None:
        self.dir_train = dir_train
        self.dir_embeddings = dir_embeddings
        self.dir_faces = dir_faces
        self.username = username
        self.mtcnn = MTCNN()
        self.in_encoder = Normalizer(norm="l2")
        self.trainX = []
        self.trainY = []
        self.model = load_model("facenet_keras.h5")

    # extract a single face from a given photograph
    def extract_face(self, image, required_size=(160, 160)):
        # convert to RGB, if needed
        image = image.convert("RGB")
        # convert to array
        pixels = asarray(image)
        # create the detector, using default weights
        detector = self.mtcnn
        # detect faces in the image
        results = detector.detect_faces(pixels)
        # extract the bounding box from the first face
        x1, y1, width, height = results[0]["box"]
        # bug fix
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height
        # extract the face
        face = pixels[y1:y2, x1:x2]
        # resize pixels to the model size
        image = Image.fromarray(face)
        image = image.resize(required_size)
        face_array = asarray(image)
        return face_array

    # load images and extract faces for all images in a directory
    def load_faces(self, directory):
        faces = list()
        # enumerate files
        for filename in os.listdir(directory):
            # path
            path = os.path.join(directory, filename)
            # get face
            face = self.extract_face(image=Image.open(path))
            # store
            faces.append(face)
        return faces

    def load_photos(self, dir) -> None:
        # enumerate folders, on per class
        path = os.path.join(dir, self.username)
        if os.path.isdir(path):
            # path
            path = os.path.join(dir, self.username)
            # load all faces in the subdirectory
            faces = self.load_faces(path)
            # create labels
            labels = [self.username for _ in range(len(faces))]
            # summarize progress
            logger.info(
                "Loaded %d examples for class: %s" % (len(faces), self.username)
            )
            # store
            self.trainX.extend(faces)
            self.trainY.extend(labels)
            return True
        else:
            raise Exception("No user photo found")

    def _get_embedding(self, face_pixels):
        # scale pixel values
        face_pixels = face_pixels.astype("float32")
        # standardize pixel values across channels (global)
        mean, std = face_pixels.mean(), face_pixels.std()
        face_pixels = (face_pixels - mean) / std
        # transform face into one sample
        samples = expand_dims(face_pixels, axis=0)
        # make prediction to get embedding
        yhat = self.model.predict(samples)
        return yhat[0]

    def _get_embeddings(self) -> tuple:
        newTrainX = list()
        for face_pixels in self.trainX:
            embedding = self._get_embedding(face_pixels)
            newTrainX.append(embedding)
        newTrainX = asarray(newTrainX)
        self.trainX = newTrainX
        logger.info(f"Created embeddings for {self.username}")
        return True

    def _save_npz(self, path, filename):
        if os.path.isdir(path):
            savez_compressed(os.path.join(path, filename), self.trainX, self.trainY)
            logger.info(f"Saved npz for filename {filename}")
        else:
            try:
                path = os.path.join(os.getcwd(), path)
                os.makedirs(path)
                savez_compressed(os.path.join(path, filename), self.trainX, self.trainY)
            except OSError as e:
                logger.exception(
                    f"Error while generating directory for {self.username}"
                )

    def _normilization(self):
        self.trainX = self.in_encoder.transform(self.trainX)
        self._save_npz(
            os.path.join(self.dir_embeddings, self.username),
            f"{self.username}_embeddings.npz",
        )

    def setup(self):
        self.load_photos(self.dir_train)
        self._save_npz(
            os.path.join(self.dir_faces, self.username), f"{self.username}_dataset.npz"
        )
        self._get_embeddings()
        self._normilization()

    def get_embedding(self, image):
        face = self.extract_face(image)

        return self._get_embedding(face)


if __name__ == "__main__":
    facenet = EmbeddingGenerator(
        "store/face_db_photos",
        "store/face_db_embeddings",
        "store/face_db_faces",
        "test",
    )
    facenet.setup()
