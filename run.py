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
    cal_posx = [[]]
    cal_posy = [[]]
    edges = [(0, 0)] * 4  # [top right, bottom right, bottom left, top left]

    size = pyautogui.size()
    pastx = [size[0] // 2] * 15
    pasty = [size[1] // 2] * 15
    print("Calibrating state 4")
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
            if cal_state != 0:
                cal_posx[-1].append((lx + rx) // 2)
                cal_posy[-1].append((ly + ry) // 2)
                if cal_count == 0:
                    cal_state -= 1
                    print(f"Calibrating state {cal_state}")
                    cal_count = cal_frames
                    print(sum(cal_posx[-1]) // len(cal_posx[-1]), sum(cal_posy[-1]) // len(cal_posy[-1]))
                    cal_posx.append([])
                    cal_posy.append([])
                else:
                    cal_count -= 1
                continue
            else:
                calibrated = True
                for i in range(4):
                    edges[i] = sum(cal_posx[i]) // len(cal_posx[i]), sum(cal_posy[i]) // len(cal_posy[i])
                RANGE_X[0] = abs(((edges[2][0] + edges[3][0]) // 2) - ((edges[0][0] + edges[1][0]) // 2))
                RANGE_Y[0] = abs(((edges[1][1] + edges[2][1]) // 2) - ((edges[0][1] + edges[3][1]) // 2))
                print("Calibrated")
                print(RANGE_X, RANGE_Y)

        # moving average of 15 frames
        pastx.insert(0, size[0] * ((lx + rx) // 2 + RANGE_X[0] // 2) // RANGE_X[0])
        del pastx[-1]
        pasty.insert(0, size[1] * ((ly + ry) // 2 + RANGE_Y[0] // 2) // RANGE_Y[0])
        del pasty[-1]

        pyautogui.moveTo(sum(pastx) // len(pastx), sum(pasty) // len(pasty))

    cap.release()
    cv2.destroyAllWindows()
