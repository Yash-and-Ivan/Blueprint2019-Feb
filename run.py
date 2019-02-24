from eye_recognition.eye_recognizer import EyeRecognizer
import cv2

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    recoginzer = EyeRecognizer(cap)

    while True:

        info = recoginzer.get_new_info()  # simon work with this :)

        print(info)

        if cv2.waitKey(int(1000/30)) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
