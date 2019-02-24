from eye_recognition.eye_recognizer import EyeRecognizer, RANGE_X, RANGE_Y
import cv2
import pyautogui

CAMERA = 1

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
    calibrated = False
    cal_state = 4
    cal_count = cal_frames = 1 * 30  # seconds * frames / second
    cal_pos = [[]]
    edges = [0] * 4  # [top right, bottom right, bottom left, top left]

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
            lx = rx = info["right_eye"]["position"][0]
            ly = ry = info["right_eye"]["position"][1]

        if not calibrated:
            print(f"Calibrating state {cal_state}")
            if cal_state != 0:
                cal_pos[-1].append(((lx + rx) // 2, (ly + ry) // 2))
                if cal_count == 0:
                    cal_state -= 1
                    cal_count = cal_frames
                else:
                    cal_count -= 1
                continue
            else:
                calibrated = True
                for i in range(4):
                    edges[i] = sum(cal_pos[i]) // len(cal_pos[i])

        print("Calibrated")

        # moving average of 15 frames
        pastx.insert(0, size[0] * ((lx + rx) // 2 + RANGE_X // 2) // RANGE_X)
        del pastx[-1]
        pasty.insert(0, size[1] * ((ly + ry) // 2 + RANGE_Y // 2) // RANGE_Y)
        del pasty[-1]

        pyautogui.moveTo(sum(pastx) // len(pastx), sum(pasty) // len(pasty))

    cap.release()
    cv2.destroyAllWindows()
