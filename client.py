import cv2
import numpy
import socket
import base64
import time


IP = "127.0.0.1" #The IP address for the localhost
PORT = 1234

sleep_time = 3 #Time in seconds for the camera to warm up
msg = b'' #Initilializes the msg string to an empty binary string
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP,PORT))

frames_sent = 0 #initliazes the number of video frames sent to 0

def stream():
    global frames_sent
    sig = 1 #signal for the video stream to keep going

    while True:
        cap = cv2.VideoCapture(0) #Captures video from the webcam
        time.sleep(sleep_time) #pauses the program to allow the camera to warm up for the time set above
        
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret==True:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    sig = 0 #
                    break
                else:
                    vid = cv2.imencode('.jpg', frame)[1] #encodes the video frame into a jpg image
                    vid_str = vid.tostring() #converts the image to a binary string
                    msg = bytes(f'{len(vid_str)}', 'utf-8') + vid_str + bytes("END", 'utf-8') #adds the length of the frame to start of the string
                    client_socket.send(msg) #sends the string to the server through the socket
                    confirmation_msg = client_socket.recv(100) #Receives the acknowledgement message from the server after sending the frame
                    frames_sent += 1 #Counts the frames sent
            else:
                print("Error capturing video!")
                break
        if sig == 0:#To break out of the while True loop
            print("Exiting program now")
            break
 
    cap.release() 
    cv2.destroyAllWindows()
    return

if __name__=='__main__':
    stream()
