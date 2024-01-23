#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch


import struct

# Declare motors 
#left_motor = Motor(Port.B)
#right_motor = Motor(Port.C)
#steer_motor = Motor(Port.A)
forward = 0
left = 0


# Auto center steering wheels.
#steer_motor.run_until_stalled(250)
#steer_motor.reset_angle(80)
#steer_motor.run_target(300,0)


# A helper function for converting stick values (0 - 255)
# to more usable numbers (-100 - 100)
def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
 
    val: float or int
    src: tuple
    dst: tuple
 
    example: print(scale(99, (0.0, 99.0), (-1.0, +1.0)))
    """
    return (float(val-src[0]) / (src[1]-src[0])) * (dst[1]-dst[0])+dst[0]


# Open the Gamepad event file:
# /dev/input/event3 is for PS3 gamepad
# /dev/input/event4 is for PS4 gamepad
# look at contents of /proc/bus/input/devices if either one of them doesn't work.
# use 'cat /proc/bus/input/devices' and look for the event file.
infile_path = "/dev/input/event4"

# open file in binary mode
in_file = open(infile_path, "rb")

# Read from the file
# long int, long int, unsigned short, unsigned short, unsigned int
FORMAT = 'llHHI'    
EVENT_SIZE = struct.calcsize(FORMAT)
event = in_file.read(EVENT_SIZE)


while event:

    (tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)

    # Handle PS4 controller left joystick
    if ev_type == 3 and code == 1:
        left = scale(value, (0,255), (-100,100))
        #if(left > 2 and left < -2):
        print("Left X1: " + str(left))
        #forward = scale(value, (0,255), (-100,100))
    if ev_type == 3 and code == 0:
        left = scale(value, (0,255), (-100,100))
        if(left > 2 and left < -2):
            print("Left Y1: " + str(left))


    #  Handle PS4 controller right joystick
    if ev_type == 3 and code == 0:
        right = scale(value, (0,255), (-100,100))
        if(right > 2 and right < -2):
            print("Right X1: " + str(left))
    if ev_type == 3 and code == 0:
        right = scale(value, (0,255), (-100,100))

        if(right > 2 and right < -2):
            print("Right Y1: " + str(left))

        


  
    if ev_type != 3 and ev_type != 0:
        print("Event type %u, code %u, value %u at %d.%d" % \
            (ev_type, code, value, tv_sec, tv_usec))
        
    # Handle PS4 controller buttons
    if ev_type == 1:
        print("Button: " + str(code) + " Value: " + str(value));
    
        # Handle PS4 controller X button
        if code == 304 and value == 1:
            ev3.speaker.say("Fire")
        # Handle PS4 controller CIRCLE(305) button
        # Handle PS4 controller SQUARE(308) button
        # Handle PS4 controller TRIANGLE(307) button
            

        # Handle PS4 controller L1(310) button
        # Handle PS4 controller L2(312) button
        # Handle PS4 controller R1(311) button
        # Handle PS4 controller R2(313) button

        # Handle PS4 controller SHARE(314) button
        # Handle PS4 controller OPTIONS(315) button
        # Handle PS4 controller PS(316) button
        # Handle PS4 controller L3(317) button
        # Handle PS4 controller R3(318) button
                    

    # Finally, read another event
    event = in_file.read(EVENT_SIZE)

in_file.close()