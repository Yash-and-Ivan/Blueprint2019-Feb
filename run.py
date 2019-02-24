from eye_recognition.eye_recognizer import EyeRecognizer, RANGE_X, RANGE_Y
import cv2
import pyautogui

CAMERA = 0

if __name__ == '__main__':
    print("Starting...")

    cap = cv2.VideoCapture(CAMERA)
    recoginzer = EyeRecognizer(cap)

    print("""
         8888888888                       
         888                              
         888                              
888  888 8888888   888  888  .d88b.       
888  888 888       888  888 d8P  Y8b      
888  888 888       888  888 88888888      
Y88b 888 888       Y88b 888 Y8b.          
 "Y88888 8888888888 "Y88888  "Y8888       
                        888               
                   Y8b d88P               
                    "Y88P" 
            """)

    size = pyautogui.size()
    pastx = [size[0] // 2] * 10
    pasty = [size[1] // 2] * 10
    past_click = [False] * 10

    while True:
        # escape to exit
        if cv2.waitKey(int(1000 / 100)) == 27:
            break

        info = recoginzer.get_new_info()  # simon work with this :)
        # eyes not detected
        if not info["status"]:
            continue

        blink = False

        if info["left_eye"]["status"] and info["right_eye"]["status"]:
            lx = info["left_eye"]["position"][0]
            ly = info["left_eye"]["position"][1]
            rx = info["right_eye"]["position"][0]
            ry = info["right_eye"]["position"][1]
        elif not info["left_eye"]["status"]:
            blink = True
        else:
            continue

        # moving average of 10 frames
        pastx.insert(0, size[0] * ((lx + rx) // 2 + RANGE_X // 2) // RANGE_X)
        del pastx[-1]
        pasty.insert(0, size[1] * ((ly + ry) // 2 + RANGE_Y // 2) // RANGE_Y)
        del pasty[-1]
        past_click.insert(0, blink)
        del past_click[-1]
        pyautogui.moveTo(sum(pastx) // len(pastx), sum(pasty) // len(pasty))

    cap.release()
    cv2.destroyAllWindows()
