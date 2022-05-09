import dlib
from scipy.spatial import distance as dist
from imutils import face_utils, resize
import numpy as np
import cv2
from imutils.video import VideoStream
from structlog import get_logger
import time
from utils.validation import EmbeddingGenerator, verification
from config.settings import (
    FACE_DB_PHOTOS_PATH,
    FACE_DB_EMBEDDINGS_PATH,
    FACE_DB_FACES_PATH,
)

logger = get_logger()


class MouthDetector:
    def __init__(self, MOUTH_AR_THRESH, username, model):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.MOUTH_AR_THRESH = MOUTH_AR_THRESH
        self.counter = 0
        self.mStart = 49
        self.mEnd = 68
        self.total = 0
        self.facenet = model
        self.username = username

    def mouth_aspect_ratio(self, mouth):
        # compute the euclidean distances between the two sets of
        # vertical mouth landmarks (x, y)-coordinates
        A = dist.euclidean(mouth[2], mouth[10])  # 51, 59
        B = dist.euclidean(mouth[4], mouth[8])  # 53, 57

        # compute the euclidean distance between the horizontal
        # mouth landmark (x, y)-coordinates
        C = dist.euclidean(mouth[0], mouth[6])  # 49, 55

        # compute the mouth aspect ratio
        mar = (A + B) / (2.0 * C)

        # return the mouth aspect ratio
        return mar

    def mouth_open_detect(self, image):
        frame = resize(image, width=640)
        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame
        rects = self.detector(gray_img, 0)
        if not rects:
            logger.error("Mouth open detector found no face")
            return None
        if len(rects) > 1:
            logger.error("Mouth open detector found more than one face")
            return None
        rect = rects[0]
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = self.predictor(gray_img, rect)
        shape = face_utils.shape_to_np(shape)

        # extract the mouth coordinates, then use the
        # coordinates to compute the mouth aspect ratio
        mouth = shape[self.mStart : self.mEnd]

        mouthMAR = self.mouth_aspect_ratio(mouth)
        mar = mouthMAR

        # check to see if the eye aspect ratio is below the blink
        # threshold, and if so, increment the blink frame counter
        if mar > self.MOUTH_AR_THRESH:
            self.counter += 1
        elif mar < self.MOUTH_AR_THRESH and self.counter > 0:
            self.total += 1
            self.counter = 0
            logger.info("Mouth open detected")

    def check(self, num_mouth_opens, images):
        self.facenet.username = self.username
        for image in images:
            self.mouth_open_detect(image=np.array(image))
            if self.counter != 0 and self.total % 2 == 0:
                verified, results = verification(self.facenet, image, self.username)
                if not verified:
                    return False, "User missmatch"
        logger.info(f"Total mouth opens is {self.total}")
        if self.total < num_mouth_opens:
            logger.error("Mouth verification unsuccessfull")
            return False
        logger.info("Mouth verification successfull")
        return True

    def video_capture(self):
        vs = VideoStream(src=0).start()
        time.sleep(1.0)
        while True:
            frame = vs.read()
            self.mouth_open_detect(image=frame)
            cv2.putText(
                frame,
                "Mouth opens: {}".format(self.total),
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )

            # show the frame
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

        # do a bit of cleanup
        cv2.destroyAllWindows()
        vs.stop()


if __name__ == "__main__":
    d = MouthDetector(0.79, "test")
    d.video_capture()
