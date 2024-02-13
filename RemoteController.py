from EventHandler import EventHandler
import threading
import struct
import socket
from time import sleep

# Purpose: A class for handling commands sent from the network remote controller (from mobile or so)
class RemoteController(EventHandler, threading.Thread):
    # A flag for stopping the main loop of handling PS4 controller events
    stopped = False;
    l_left = 0;
    l_forward = 0;
    r_left = 0;
    r_forward = 0;

    # Constructor
    def __init__(self):
        super().__init__()
    def __str__(self):
        return "Remote controller"; 
    
    # This is the main loop awaiting for incoming commands from the network. Run in a separate thread.
    def run(self):

        # get the hostnam
        host = ""
        port = 27700  # initiate port no above 1024

        server_socket = socket.socket()  # get instance
        # look closely. The bind() function takes tuple as argument
        server_socket.bind((host, port))  # bind host address and port together

        # configure how many client the server can listen simultaneously
        print("Server started on: " + str(host))
        server_socket.listen(2)

        while True:
            self.establish_connection(server_socket) 

        conn.close();  # close the connection



    def establish_connection(self,server_socket):
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))
        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn.recv(1024).decode()
            if not data:
                # if data is not received break
                break
            print("from connected user: " + str(data))
            self.command_decode(data)

    def handle_event(self, event):
        # Override this method to handle PS4 controller events
        pass


    def command_decode(self,data):
        print ("Command:" + data)
        if data == "TurnLeft!":
            self.trigger("left");
        elif data == "TurnRight!":
            self.trigger("right");
        elif data == "EngineAhead!":
            self.trigger("forward");
        elif data == "EngineBack!":
            self.trigger("backward");
        elif data == "Fire!":
            self.trigger("fire");
        else:
            self.trigger("unknown");
 
    def stop(self):
        self.stopped = True;


    def onLeft(self, callback):
        self.on("left", callback)

    def onRight(self, callback):
        self.on("right", callback)


    def onForward(self, callback):
        self.on("forward", callback)


    def onBackward(self, callback):
        self.on("backward", callback)


    def onFire(self, callback):
        self.on("fire", callback)

    def onCameraLeft(self, callback):
        self.on("camera_left", callback)

    def onCameraRight(self, callback):
        self.on("camera_right", callback)
