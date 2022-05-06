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
    PHOTO_VERIFICATION_METHOD_EYE,
)

logger = get_logger()


class BlinkingDetector:
    def __init__(self, shape_predictor_filename, eye_ar_thershold, eye_ar_frames, username):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(shape_predictor_filename)
        self.eye_ar_thershold = eye_ar_thershold
        self.eye_ar_frames = eye_ar_frames
        self.counter = 0
        self.left_eye = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        self.right_eye = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
        self.total = 0
        self.facenet = EmbeddingGenerator(
            FACE_DB_PHOTOS_PATH, FACE_DB_EMBEDDINGS_PATH, FACE_DB_FACES_PATH
        )
        self.username = username

    def eye_aspect_ratio(self, eye):
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])

        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])

        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)

        # return the eye aspect ratio
        return ear

    def eye_blink_detect(self, image):
        image = resize(image, width=450)
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        rects = self.detector(gray_img, 0)
        if not rects:
            logger.error("Eye blink detector found no face")
            return None
        if len(rects) > 1:
            logger.error("Eye blink detector found more than one face")
            return None
        rect = rects[0]
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = self.predictor(gray_img, rect)
        shape = face_utils.shape_to_np(shape)

        # extract the left and right eye coordinates, then use the
        # coordinates to compute the eye aspect ratio for both eyes
        leftEye = shape[self.left_eye[0] : self.left_eye[1]]
        rightEye = shape[self.right_eye[0] : self.right_eye[1]]
        leftEAR = self.eye_aspect_ratio(leftEye)
        rightEAR = self.eye_aspect_ratio(rightEye)

        # average the eye aspect ratio together for both eyes
        ear = (leftEAR + rightEAR) / 2.0

        # check to see if the eye aspect ratio is below the blink
        # threshold, and if so, increment the blink frame counter
        if ear < self.eye_ar_thershold:
            self.counter += 1

        # otherwise, the eye aspect ratio is not below the blink
        # threshold
        else:
            # if the eyes were closed for a sufficient number of
            # then increment the total number of blinks
            if self.counter >= self.eye_ar_frames:
                logger.info("Eye blink detector detected blink")
                self.total += 1

            # reset the eye frame counter
            self.counter = 0

    def check(self, num_blinks, images):
        self.facenet.username = self.username
        for image in images:
            self.eye_blink_detect(image=image)
            if self.counter != 0:
                verified, results = verification(self.facenet, image, self.username)
                if not verified:
                    return False, "User missmatch"
        logger.info(f"Total blinks is {self.total}")
        if self.total < num_blinks:
            logger.error("Blink verification unsuccessfull")
            return False
        logger.info("Blink verification successfull")
        return True

    def video_capture(self):
        vs = VideoStream(src=0).start()
        time.sleep(1.0)
        while True:
            frame = vs.read()
            self.eye_blink_detect(image=frame)
            cv2.putText(
                frame,
                "Blinks: {}".format(self.total),
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
    d = BlinkingDetector("../shape_predictor_68_face_landmarks.dat", 0.25, 3)
    d.video_capture()
