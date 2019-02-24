from eye_recognition.eye_recognizer import EyeRecognizer, RANGE_X, RANGE_Y
import cv2
import pyautogui
import os
import face_recognition
import imutils
import numpy as np

CAMERA = 0


def uEye(face_encoding):

    cap = cv2.VideoCapture(CAMERA)
    recoginzer = EyeRecognizer(cap, face_encoding)

    calibrated = False
    cal_state = 4
    cal_count = cal_frames = 1 * 30  # seconds * frames / second
    cal_posx = [[]]
    cal_posy = [[]]
    edges = [(0, 0)] * 4  # [top right, bottom right, bottom left, top left]

    size = pyautogui.size()
    pastx = [size[0] // 2] * 10
    pasty = [size[1] // 2] * 10
    while True:
        # escape to exit
        if cv2.waitKey(int(1000 / 100)) == 27:
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
        else:
            continue

        # moving average of 10 frames
        pastx.insert(0, size[0] * ((lx + rx) // 2 + RANGE_X // 2) // RANGE_X)
        del pastx[-1]
        pasty.insert(0, size[1] * ((ly + ry) // 2 + RANGE_Y // 2) // RANGE_Y)
        del pasty[-1]

        try:
            pyautogui.moveTo(sum(pastx) // len(pastx), sum(pasty) // len(pasty))
        except BaseException:
            break

    cap.release()
    cv2.destroyAllWindows()

def list_users():
    try:
        users = eval(open('users.dat', 'r').read())
        for key in users:
            print(key)
    except FileNotFoundError:
        print("No users! Create a new user by running \'make-user\'")

def new_user(name: str):
    if not os.path.exists('users.dat'):
        f = open('users.dat', 'w+')
        f.write(str({}))
        f.close()

    users = eval(open('users.dat', 'r').read())
    if name in users:
        print("Username %s taken. Sorry!" % name)
        return

    print("Preparing to create new user")

    cap = cv2.VideoCapture(CAMERA)

    face_loc = None

    while True:
        print("Please face the camera")
        _, frame = cap.read()

        locs = face_recognition.face_locations(frame)
        locs.sort(key=lambda x: (x[2] - x[0]) * (x[3] - x[1]), reverse=True)

        if len(locs) == 0:
            print("No faces found.")
            continue

        face_loc = locs[0]

        cv2.rectangle(frame, (face_loc[3], face_loc[0]), (face_loc[1], face_loc[2]), (255, 0, 0), 1)

        cv2.imshow('Hopefully you ???', frame)

        print("Press the 'y' key to confirm that this is you. Press any other key if its not.")


        if cv2.waitKey(0) == ord('y'):
            cv2.destroyAllWindows()
            break

    face = imutils.resize(frame[face_loc[0]:face_loc[2], face_loc[3]:face_loc[1]],
                          width=500,
                          inter=cv2.INTER_CUBIC)

    face_encoding = face_recognition.face_encodings(face)

    if len(face_encoding) == 0:
        print("Something went wrong. Please run \'make-user\' again.")
        return

    face_encoding = face_encoding[0]

    users[name] = face_encoding.tolist()

    o = open('users.dat', 'w+')
    o.write(str(users))
    o.close()
    print("New user successfully created!")


if __name__ == '__main__':
    print("Starting...")
    print("""
Welcome to:

.        8888888888  .        ✦         
    .    888              ✦     *         
*        888    *                         
888  888 8888888   888  888  .d88b.       
888  888 888       888  888 d8P  Y8b      
888  888 888       888  888 88888888      
Y88b 888 888       Y88b 888 Y8b.          
 "Y88888 8888888888 "Y88888  "Y8888       
                *       888               
          ✦        Y8b d88P   ✦           
    .               "Y88P" 
                """)
    print("What do you want to do?")
    while True:

        inp = input("> ")
        inp = inp.replace(" ", '').strip().lower()

        if inp == 'help':
            print("""
Avaliable commands (more to come soon, hopefully):

help: get some help
make-user: make a new user
list-users: list all existing users
run: run uEye
exit: exit the program
            """)
        elif inp == 'exit':
            exit(0)
        elif inp == 'make-user':
            name = input("Please type in your desired username: ")
            new_user(name)
        elif inp == 'list-users':
            list_users()
        elif inp == 'run':
            username = input("Please enter your username: ")
            users = eval(open('users.dat', 'r').read())
            if username not in users:
                print("No such user exists. Create a new user with \'make-user\' or check "
                      "all existing users with \'list-users\' ")
            face_encoding = users[username]

            print("Preparing to run uEye")
            print("Either hit escape or move your mouse to the top left corner to exit")

            uEye(np.array(face_encoding))

            print("Done!")

        else:
            print('Unknown command. Type \'help\' for help')