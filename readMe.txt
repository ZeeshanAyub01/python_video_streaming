This project contains two python files:

Client.py: Captures video from the laptop's webcam, converts it to a bit string, and sends it over to the server.

Server.py: Receives video data from the client, converts it from bytes to video frames, and
displays them.

How to run the program:
1. Run server.py
2. Run client.py

   *Note: Before running client.py the IP address of the host computer will have to hardcoded into the IP variable in the client.py file. The host's IP address on the current network can be obtained by opening a terminal on the host computer and typing in 'ipconfig', and looking under the network.

To capture the current frame:
1. Press 'c'; this will store the current frame as a '.png' image in the same folder as the scripts

How to stop the program:
Go over to the python video, and press 'Esc'; pressing 'q' will NOT exit the video
