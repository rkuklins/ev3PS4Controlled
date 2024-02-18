#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from PS4Controller import MIN_JOYSTICK_MOVE, PS4Controller
from Pixy2Camera import Pixy2Camera
#from Pixy2Camera import Pixy2Camera
from RemoteController import RemoteController
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)

from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)

import sys
import math
from time import sleep

#TODO: Better understand the debug mode
if __debug__:
    print("Debug ON")
else:
    print('Debug OFF');

ev3 = EV3Brick()
steer_motor = Motor(Port.A)     #This is the main power motor
drive_L_motor = Motor(Port.B)     #This is a motor controlling steering
drive_R_motor = Motor(Port.C)   #This is a motor controlling turret
us_sensor = UltrasonicSensor(Port.S2)  #This is a sensor for distance measurement
pixy_camera = Pixy2Camera(Port.S1)  #This is a camera for object detection


#last_angle = 5

def lightoff(value):
    #us_sensor.distance();


    """
    Perform the specified action.

    Args:
        value: The value to be used for the action.

    Returns:
        None
    """

    pixy_camera.light(False);

def lighton(value):
    #us_sensor.distance();


    """
    Perform the specified action.

    Args:
        value: The value to be used for the action.

    Returns:
        None
    """

    pixy_camera.light(True);

def sayit(value):
    ev3.speaker.say("Hello, I am Wrack!")

def quit(value):
    value.stop()                                                  


def driftLeft(value):
    steer_motor.run(-1000)
    drive_L_motor.run(-1000)
    drive_R_motor.run(1000)

def driftRight(value):
    steer_motor.run(1000)
    drive_L_motor.run(1000)
    drive_R_motor.run(-1000)


def driftStop(value):
    steer_motor.stop()
    drive_L_motor.stop();
    drive_R_motor.stop();

def move(value): 
    """
    Moves the steer motor based on the provided value.

    Args:
        value: The value to control the steer motor.

    Returns:
        None
    """
    
    steer_motor.run(value.l_left)

    if (abs(value.l_forward) < MIN_JOYSTICK_MOVE):
        drive_L_motor.stop();
        drive_R_motor.stop();
    else:
        drive_L_motor.run(value.l_forward)
        drive_R_motor.run(value.l_forward)

def watch(value):
    global last_angle  

    #turret_motor.run(value.r_left*10)

    """
    result = 0;
    val_x = value.r_left * -1;
    val_y = value.r_forward;
    
    if(abs(val_x) < 10 and abs(val_y) < 10):
        return
    if(val_x == 0):
        return;

    quadrant = 1;
    if (val_x < 0 and val_y < 0):
        quadrant = 3
        #result_degrees = result_degrees_orig + 180
        result = math.atan(abs(val_x) / abs(val_y))
    elif(val_y < 0):
        quadrant = 2
        #result_degrees = result_degrees_orig + 90
        result = math.atan(abs(val_y) / abs(val_x))
    elif(val_x < 0):
        quadrant = 4
        #result_degrees = result_degrees_orig + 270
        result = math.atan(abs(val_y) / abs(val_x))
    else:
        quadrant = 1
        result = math.atan(abs(val_x) / abs(val_y))

    result_degrees_orig = math.degrees(result)
    result_degrees = result_degrees_orig

    if(quadrant == 3):
        result_degrees = result_degrees_orig + 180
    elif(quadrant==2):
        result_degrees = result_degrees_orig + 90
    elif(quadrant == 4):
        result_degrees = result_degrees_orig + 270

    #TODO: Need to improve shift not to move by small 5 degrees move if this is a move by 30 degrees. This requries to add some intertia to the move
    angle_shift = abs(result_degrees - last_angle);
    speed = 360;
    result_degrees_final = result_degrees;
    if(angle_shift > 180):
        if(result_degrees > last_angle):
            diff = result_degrees - last_angle;
            diff = diff - 360;
            result_degrees_final = last_angle + diff;
        else:
            diff = result_degrees - last_angle;
            diff = diff + 360;
            result_degrees_final = last_angle + diff;

        print("Shift is greater than 180:" + str(result_degrees_final))
        speed = -1 * speed;
    


    if(angle_shift < 5):
        return

    print(str(result_degrees_final) + " from " + str(last_angle) + " shift: " + str(angle_shift) + " speed: " + str(speed))

    drive_motor.track_target(result_degrees_final)
    last_angle = result_degrees;
    """


def blockDetected(value):
#    if(value.blocks == None or len(value.blocks) == 0):
#        return;
    block = value.blocks[0];





def main():
    """
    remoteController = RemoteController();

    remoteController.onFire(doit)

    remoteController.start()
"""
    drive_L_motor.stop();
    drive_R_motor.stop();

    controller = PS4Controller()

    pixy_camera.onBlockDetected(blockDetected);

    controller.onL1Button(lighton)
    controller.onR1Button(lightoff)
    controller.onCrossButton(sayit)
    controller.onOptionsButton(quit)
    controller.onLeftJoystickMove(move)
    controller.onLeftArrowPressed(driftLeft)
    controller.onRightArrowPressed(driftRight)
    controller.onLRArrowReleased(driftStop)
#    controller.onRightJoystickMove(watch)
    controller.start()
    pixy_camera.start()

    print ("Threads started")
    #Wait for controller thread to finish
    #controller.join()
    #pixy_camera.join();


main()
