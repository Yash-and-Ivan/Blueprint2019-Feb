from eye_recognition.eye_recognizer import EyeRecognizer, RANGE_X, RANGE_Y
import cv2
import pyautogui

CAMERA = 1
pyautogui.FAILSAFE = False

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
    pastx = [0] * 10
    pasty = [0] * 10
    blinks = [False] * 10

    calibrated = False
    lxc = []
    rxc = []
    lyc = []
    ryc = []

    lxca = 0
    rxca = 0
    lyca = 0
    ryca = 0
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
        elif not info["left_eye"]["status"] and not info["right_eye"]["status"]:
            lx = rx = size[0] // 2
            ly = ry = size[1] // 2
        elif info["left_eye"]["status"]:
            rx = lx = info["left_eye"]["position"][0]
            ry = ly = info["left_eye"]["position"][1]
        else:
            blink = True
            lx = rx = info["right_eye"]["position"][0]
            ly = ry = info["right_eye"]["position"][1]

        # moving average of 10 frames
        pastx.insert(0, (lx - lxca + rx - rxca) // 2)
        del pastx[-1]
        pasty.insert(0, (ly - lyca + ry - ryca) // -2)
        del pasty[-1]
        blinks.insert(0, blink)
        del blinks[-1]

        if not calibrated:
            print("Please look at the middle of the screen")
            if len(lyc) == 50:
                lxca = sum(lxc) // len(lxc)
                rxca = sum(rxc) // len(rxc)
                lyca = sum(lyc) // len(lyc)
                ryca = sum(ryc) // len(ryc)
                print(lyca, ryca)
                calibrated = True
            else:
                lxc.append(lx)
                rxc.append(rx)
                lyc.append(ly)
                ryc.append(ry)
        else:
            (pyautogui.drag if blinks.count(True) > 5 else pyautogui.move)(sum(pastx) // len(pastx),
                                                                           sum(pasty) // len(pasty))

    cap.release()
    cv2.destroyAllWindows()
