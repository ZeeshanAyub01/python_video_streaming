import cv2
import numpy
import socket
import base64
import time

MSG_LENGTH = 4096*4 #Size of the Chunk of data to accept at any one time
HDR_LENGTH = 5 #predefined length of the header, that contains the size of the incoming video frame
IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#To allow the sockets to use the same port again
server_socket.bind((IP,PORT))
server_socket.listen()


data = b'' #the variable to store incoming data
frame_end = 0 #end of video frame
incomp_frames = 0 #number of incomplete frames receieved
num_frames = 0 #number of complete frames received
start = 0
end = 0
display_time = 0

while True:
    client_socket, client_address = server_socket.accept()

    while True:
        msg = client_socket.recv(MSG_LENGTH)
        client_socket.send(bytes("OK",'utf-8'))

        if len(msg):#Only operates on the received data, if its size is greater than 0
            data += msg
            frame_end = data.find(b'END')

            if start == 0:
                    start = time.time()

            if frame_end > 0:
                num_frames += 1
                video_bytes = data[HDR_LENGTH:frame_end] #
                print(f"Current frame size: {len(video_bytes)}") #Line added for debugging purposes
                nparr = numpy.frombuffer(video_bytes, numpy.uint8) #Converts the data received from bytes to a numpy array
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR) #Converts the numpy array to a video frame
                data = b'' #restores 'data' variable to an empty binary string
                frame_end = 0 #restores frame_end to 0
                incomp_frames = 0 #restores incomp_frames to 0
                client_socket.send(bytes("Full frame received",'utf-8')) #Acknowledgment for receiving a full frame
                try:
                    cv2.imshow("Stream", frame) #Displays the received frame
                    if cv2.waitKey(2) & 0xFF == ord('q'): #to display the current frame indefinitely
                        flag = 0
                        display_time = time.time() - start
                        break
                except Exception as e:
                    #print(e)
                    #print(f"{type(frame)}, {frame_end}")
                    pass
            else:
                incomp_frames += 1 #Counts the incomplete frames received
            
        else: #quits the program if the the received data size is 0
            flag = 0
            break
    
    if flag == 0: #Flag to signal the end of data streaming
        print(f"Exiting progam now; displayed a total of {num_frames} frames in {display_time} seconds, with an average rate of { num_frames / display_time } frames per second")
        break
