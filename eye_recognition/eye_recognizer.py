import face_recognition
import dlib
from imutils import face_utils
import imutils
import numpy as np
import cv2

RANGE_X = 200
RANGE_Y = 50

class EyeRecognizer():
    def get_new_info(self):

        back = {}

        ret, frame = self._cap.read()

        if not ret:
            back['status'] = False
            return back

        face_locs = face_recognition.face_locations(frame, 0, 2 ** 14)  # get all faces
        face_locs.sort(key=lambda x: (x[2] - x[0]) * (x[3] - x[1]), reverse=True)  # sort by area

        if len(face_locs) == 0:  # no faces found
            back['status'] = False
            return back

        face_loc = face_locs[0]

        face = imutils.resize(frame[face_loc[0]:face_loc[2], face_loc[3]:face_loc[1]],
                              width=500,
                              inter=cv2.INTER_CUBIC)  # resize frame

        face_w, face_h, _ = face.shape

        face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        face_points = face_utils.shape_to_np(self._face_predictor(face_gray, dlib.rectangle(0, 0, face_w, face_h)))

        if not len(face_points) == 68:
            back['status'] = False
            return back

        left_eye_i, left_eye_j = face_utils.FACIAL_LANDMARKS_68_IDXS['left_eye']
        right_eye_i, right_eye_j = face_utils.FACIAL_LANDMARKS_68_IDXS['right_eye']

        left_eye = [(x, y) for x, y in face_points[left_eye_i:left_eye_j]]
        right_eye = [(x, y) for x, y in face_points[right_eye_i:right_eye_j]]

        left_eye_bounding_rect = cv2.boundingRect(np.array([left_eye]))
        right_eye_bounding_rect = cv2.boundingRect(np.array([right_eye]))

        left_eye_info = self._get_eye_info(face, left_eye_bounding_rect, 'left eye')
        right_eye_info = self._get_eye_info(face, right_eye_bounding_rect, 'right eye')

        back['status'] = True
        back['left_eye'] = left_eye_info
        back['right_eye'] = right_eye_info

        return back

    def _get_eye_info(self, face: np.array, bounding_rect: tuple, name: str):
        back = {}

        face_w, face_h, _ = face.shape
        eye_middle = int(bounding_rect[1] + bounding_rect[3] / 2)
        eye_half_width = int(bounding_rect[2] / 2)
        eye = face[(eye_middle - eye_half_width):(eye_middle + eye_half_width),
              bounding_rect[0]:(bounding_rect[0] + bounding_rect[2])]

        # prepare image for hough circles
        eye = imutils.resize(eye, width=250, inter=cv2.INTER_CUBIC)
        # eye = cv2.GaussianBlur(eye, (9, 9), 2, 2)
        eye_gray = cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY)
        eye_gray = cv2.addWeighted(eye_gray, 2, eye_gray, 0, 0)  # brighten the image
        eye_gray = cv2.morphologyEx(eye_gray, cv2.MORPH_CLOSE, (20, 20))

        circles = cv2.HoughCircles(eye_gray, cv2.HOUGH_GRADIENT, 1, 25,
                                   param1=30, param2=30, minRadius=10, maxRadius=75)

        if circles is None or len(circles.shape) != 3:
            cv2.imshow(name, eye)
            back['status'] = False
            return back

        pupil = sorted(circles[0], key=lambda x: self._average_brightness(eye_gray, x))[0]

        cv2.rectangle(eye, (125 - RANGE_X//2, 125 - RANGE_Y//2), (125 + RANGE_X//2, 125 + RANGE_Y//2), (255, 255, 0), 1)
        cv2.line(eye, (0, pupil[1]), (250, pupil[1]), (0, 255, 0), 1)
        cv2.line(eye, (pupil[0], 0), (pupil[0], 250), (0, 255, 0), 1)
        cv2.circle(eye, (pupil[0], pupil[1]), pupil[2], (255, 0, 0), 3)
        cv2.circle(eye, (pupil[0], pupil[1]), 3, (0, 0, 255), -1)

        back['status'] = True
        back['position'] = (125 - pupil[0], 125 - pupil[1])
        back['radius'] = pupil[2]
        back['num_circles'] = len(circles[0])

        cv2.imshow(name, eye)

        return back

    def _average_brightness(self, img, circle):
        zero_img1 = np.zeros((img.shape[0], img.shape[1]), np.uint8)
        zero_img2 = np.zeros((img.shape[0], img.shape[1]), np.uint8)
        cv2.circle(zero_img1, (circle[0], circle[1]), circle[2], (255, 255, 255), -1)
        cv2.circle(zero_img2, (circle[0], circle[1]), int(circle[2] + 10), (255, 255, 255), 5)
        return (cv2.mean(img, mask=zero_img1))[0] - (cv2.mean(img, mask=zero_img2))[0]

    def __init__(self, cap: cv2.VideoCapture):
        self._cap = cap
        self._face_predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    def __del__(self):
        pass
