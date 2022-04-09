from numpy import load, sum, array
from sklearn.preprocessing import Normalizer
from scipy import spatial
import argparse
import structlog
from embedding_generator import EmbeddingGenerator

logger = structlog.get_logger()


def verify(input_image, embeddings, detection_threshold, verification_threshold):
    # Build results array
    results = []
    for validation_image in embeddings:
        # Make Predictions
        result = spatial.distance.cosine(input_image, validation_image)
        logger.info(f"Distance between 2 embeddings is {result}")
        results.append(result)

    # Detection Threshold: Metric above which a prediciton is considered positive
    detection = sum(array(results) < detection_threshold)
    # Verification Threshold: Proportion of positive predictions / total positive samples
    verification = detection / len(embeddings)
    verified = verification > verification_threshold

    return results, verified


def verification(model, image, username):
    input_embedding = model.get_embedding(image)

    try:
        data = load(f"face_db_embeddings/{username}/{username}_embeddings.npz")
        embeddings = data["arr_0"]

    except FileNotFoundError:
        print("No file found")

    # in_encoder = Normalizer(norm="l2")

    # embeddings = in_encoder.transform(embeddings)
    # input_embedding = in_encoder.transform(input_embedding)

    results, verified = verify(
        input_image=input_embedding,
        embeddings=embeddings,
        detection_threshold=0.3,
        verification_threshold=0.6,
    )
    if verified:
        logger.info("You are welcome")
        return True
    else:
        logger.error("Blocked")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Procces validation through username.")
    parser.add_argument("-u", dest="username", required=True)
    args = parser.parse_args()
    image = []
    verification(image, args.username)
