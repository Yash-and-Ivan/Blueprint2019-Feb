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
    pastx = [size[0] // 2] * 15
    pasty = [size[1] // 2] * 15
    while True:
        # escape to exit
        if cv2.waitKey(int(1000 / 30)) == 27:
            break

        info = recoginzer.get_new_info()  # simon work with this :)

        # eyes not detected
        if not info["status"]:
            continue

        # left click
        if not info["left_eye"]["status"]:
            continue

        # right click
        if not info["right_eye"]["status"]:
            continue

        lx = info["left_eye"]["position"][0]
        ly = info["left_eye"]["position"][1]
        rx = info["right_eye"]["position"][0]
        ry = info["right_eye"]["position"][1]

        # moving average of 15 frames
        pastx.insert(0, size[0] * ((lx + rx) // 2 + RANGE_X // 2) // RANGE_X)
        del pastx[-1]
        pasty.insert(0, size[1] * ((ly + ry) // 2 + RANGE_Y // 2) // RANGE_Y)
        del pasty[-1]

        pyautogui.moveTo(sum(pastx) // len(pastx), sum(pasty) // len(pasty))

    cap.release()
    cv2.destroyAllWindows()
