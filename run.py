from eye_recognition.eye_recognizer import EyeRecognizer
import cv2

CAMERA = 0

if __name__ == '__main__':
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

    while True:


        info = recoginzer.get_new_info()  # simon work with this :)

        print(info)

        if cv2.waitKey(int(1000/30)) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
