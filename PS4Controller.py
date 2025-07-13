import math
from EventHandler import EventHandler
import threading
import struct
import traceback
from time import sleep

MIN_JOYSTICK_MOVE = 15  # The minimum value of joystick move to be considered as a move
    #const values representing particular events 

#ev_type
EV_SYN = 0;
EV_KEY = 1;
EV_ABS = 3;

#ev_code (for ev_type == EV_KEY)
X_BUTTON = 304;
CIRCLE_BUTTON = 305;
TRIANGLE_BUTTON = 307;
SQUARE_BUTTON = 308;

#ev_code (for ev_type == EV_ABS)
LEFT_STICK_X = 0;
LEFT_STICK_Y = 1;
RIGHT_STICK_X = 3;
RIGHT_STICK_Y = 4;
L2_TRIGGER = 3;
R2_TRIGGER = 4;


def printIn(x,y,text):
    #Prints text in str value in x,y coordinates on console
    if __debug__:
        print("\033["+str(y)+";"+str(x)+"H"+text)


# Purpose: A class for handling PS4 controller events.
class PS4Controller(EventHandler, threading.Thread):

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
        return "PS4 controller for EV3"; 
    
    # This is the main loop of handling PS4 controller events. It is run in a separate thread.
    def run(self):
       # Open the Gamepad event file:
        # /dev/input/event3 is for PS3 gamepad
        # /dev/input/event4 is for PS4 gamepad
        # look at contents of /proc/bus/input/devices if either one of them doesn't work.
        # use 'cat /proc/bus/input/devices' and look for the event file.
        infile_path = "/dev/input/event4"
        
        try:
            # open file in binary mode
            in_file = open(infile_path, "rb")

            # Read from the file
            # long int, long int, unsigned short, unsigned short, unsigned int
            FORMAT = 'llHHI'    
            EVENT_SIZE = struct.calcsize(FORMAT)
            event = in_file.read(EVENT_SIZE)
            i = 0;
            
            if __debug__:
                print("Starting the PS4 loop...")            
            while event and not self.stopped:
                (tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)


                #  Handle PS4 controller right joystick
                if ev_type == EV_ABS and (code == RIGHT_STICK_X or code == RIGHT_STICK_Y):
                    if(code == RIGHT_STICK_Y):
                        self.r_forward = -1* self.scale(value, (0,255), (-100,100))
                        printIn(35,11,"Right y-axis:" + str(self.r_forward) + "   ")                        
                    if(code == RIGHT_STICK_X):
                        self.r_left = -1 * self.scale(value, (0,255), (-100,100))
                        printIn(35,10,"Right x-axis:" + str(self.r_left) + "   ")   

                    if (abs(self.r_forward) > 10 or abs(self.r_left) > MIN_JOYSTICK_MOVE):
                        self.trigger("right_joystick");

                # Handle PS4 controller left joystick
                if ev_type == EV_ABS and (code == LEFT_STICK_X or code == LEFT_STICK_Y):
                    if(code == LEFT_STICK_Y and value < 255):                                             
                        self.l_forward = self.scale(value, (0,255), (-1000,1000))
                        printIn(1,11,"Left y-axis:" + str(self.l_forward)+ "   ")   
                    if(code == LEFT_STICK_X and value < 255):
                        self.l_left = self.scale(value, (0,255), (-100,100))
                        printIn(1,10,"Left x-axis:" + str(self.l_left ) + "   ")                        

                    if (abs(self.l_forward) > MIN_JOYSTICK_MOVE or abs(self.l_left) > MIN_JOYSTICK_MOVE):
                        if(abs(self.l_forward) < MIN_JOYSTICK_MOVE):
                            self.l_forward = 0;
                        if(abs(self.l_left) < MIN_JOYSTICK_MOVE):
                            self.l_left = 0;    
                        self.trigger("left_joystick");




                #Handle the pad
                if ev_type == 3 and code >15:
                    if(code == 16 and value == 1):
                        self.trigger("left_arrow_pressed");
                    if(code == 16 and value == 0):
                        self.trigger("lr_arrow_released");
                    if(code == 16 and value == 4294967295):
                        self.trigger("right_arrow_pressed");

                # Handle PS4 controller buttons
                if ev_type == EV_KEY:
                    printIn(1,15,"Button code:" + str(code) + "   ")
                    #TODO: Change it all into case statement
                    # Handle PS4 controller X button
                    if code == 304 and value == 1:
                        self.trigger("cross_button");
                    #Handle PS4 controller CIRCLE(305) button
                    if code == 305 and value == 1:
                        self.trigger("triangle_button");
                    #Handle PS4 controller SQUARE(308) button
                    if code == 308 and value == 1:
                        self.trigger("triangle_button");
                    # Handle PS4 controller TRIANGLE(307) button
                    if code == 307 and value == 1:
                        self.trigger("triangle_button");
                    

                    #Handle PS4 controller L1(310) button
                    if code == 310 and value == 1:
                        self.trigger("l1_button");
                    #Handle PS4 controller L2(312) button
                    if code == 312 and value == 1:
                        self.trigger("l2_button");
                    #Handle PS4 controller R1(311) button
                    if code == 311 and value == 1:
                        self.trigger("r1_button");
                    #Handle PS4 controller R2(313) button
                    if code == 313 and value == 1:
                        self.trigger("r2_button");

                    # TODO: Handle PS4 controller SHARE(314) button
                    # TODO: Handle PS4 controller OPTIONS(315) button
                    if code == 315 and value == 1:
                        self.trigger("options_button");
                    # TODO: Handle PS4 controller PS(316) button
                    # TODO: Handle PS4 controller L3(317) button
                    # TODO: Handle PS4 controller R3(318) button

                sleep(0.01)            
                # Finally, read another event
                event = in_file.read(EVENT_SIZE)
                

            in_file.close()
        except Exception as e:
            if __debug__:
                print("Error occurred:", str(e))
                traceback.print_exc()

    def handle_event(self, event):
        # Override this method to handle PS4 controller events
        pass
 
    def stop(self):
        self.stopped = True;

    # A helper function for converting stick values (0 - 255)
    # to more usable numbers (-100 - 100)6
    def scale(self, val, src, dst):
        """
        Scale the given value from the scale of src to the scale of dst.
    
        val: float or int
        src: tuple
        dst: tuple
   
        example: print(scale(99, (0.0, 99.0), (-1.0, +1.0)))
        """
        return (float(val-src[0]) / (src[1]-src[0])) * (dst[1]-dst[0])+dst[0]

    def onLeftJoystickMove(self, callback):
        self.on("left_joystick", callback)

    def onRightJoystickMove(self, callback):
        self.on("right_joystick", callback)

    def onSquareButton(self, callback):
        self.on("square_button", callback)

    def onCrossButton(self, callback):
        self.on("cross_button", callback)

    def onTriangleButton(self, callback):
        self.on("triangle_button", callback)

    def onCircleButton(self, callback):
        self.on("circle_button", callback)

    def onL1Button(self, callback):
        self.on("l1_button", callback)

    def onR1Button(self, callback):
        self.on("r1_button", callback)

    def onL2Button(self, callback):
        self.on("l2_button", callback)

    def onR2Button(self, callback):
        self.on("r2_button", callback)

    def onOptionsButton(self, callback):
        self.on("options_button", callback)

    def onLeftArrowPressed(self, callback):
        self.on("left_arrow_pressed", callback)

    def onLRArrowReleased(self, callback):
        self.on("lr_arrow_released", callback)

    def onRightArrowPressed(self, callback):
        self.on("right_arrow_pressed", callback)

