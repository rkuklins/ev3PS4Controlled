#!/usr/bin/env pybricks-micropython

"""
EV3 PS4 Controller Robot with Graceful Device Handling

This program controls an EV3 robot using a PS4 controller with robust
device management that handles missing devices gracefully.

Features:
- Automatic device detection and initialization
- Graceful handling of missing devices
- Safe device operations with error handling
- Device status reporting and debugging
- Conditional feature activation based on device availability

Device Manager:
The DeviceManager class provides a centralized way to handle all EV3 devices
with proper error handling. It automatically detects which devices are
connected and provides safe access methods.

Usage:
- Devices are automatically initialized on startup
- Use device_manager.is_device_available() to check if a device exists
- Use device_manager.safe_device_call() for safe device operations
- Use device_manager.safe_device_operation() for complex operations
"""

from pybricks.hubs import EV3Brick
from PS4Controller import MIN_JOYSTICK_MOVE, PS4Controller
from Pixy2Camera import Pixy2Camera
from DeviceManager import DeviceManager
from RemoteController import RemoteController
from TankDriveSystem import TankDriveSystem
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

# Initialize device manager
device_manager = DeviceManager()

# Global state to avoid redundant stop calls
robot_is_stopped = False

# Initialize devices with graceful error handling
drive_L_motor = device_manager.try_init_device(Motor, Port.D, "drive_L_motor")
drive_R_motor = device_manager.try_init_device(Motor, Port.B, "drive_R_motor")
#turret_motor = device_manager.try_init_device(Motor, Port.D, "turret_motor")
#us_sensor = device_manager.try_init_device(UltrasonicSensor, Port.S2, "us_sensor")
#pixy_camera = device_manager.try_init_device(Pixy2Camera, Port.S1, "pixy_camera")

# Initialize drive system
tank_drive_system = TankDriveSystem(device_manager)
tank_drive_system.initialize()

# Print device status
device_manager.print_device_status()

def test_device_management():
    """
    Test function to demonstrate device management capabilities.
    This function shows how to safely work with devices.
    """
    print("=== Testing Device Management ===")
    
    # Test individual device availability
    print("Steer motor available: {}".format(device_manager.is_device_available('steer_motor')))
    print("Drive motors available: {}".format(device_manager.are_devices_available(['drive_L_motor', 'drive_R_motor'])))
    
    # Test safe device calls
    device_manager.safe_device_call("steer_motor", "stop")
    device_manager.safe_device_call("pixy_camera", "light", True)
    
    # Test complex operations
    def complex_motor_operation(motor, speed, duration):
        """Example of a complex motor operation"""
        motor.run(speed)
        sleep(duration)
        motor.stop()
        return "Operation completed"
    
    result = device_manager.safe_device_operation(
        "steer_motor", 
        "complex_motor_test", 
        complex_motor_operation, 
        500,  # speed
        1     # duration
    )
    
    if result:
        print("Complex operation result: {}".format(result))
    
    # Get device summary
    summary = device_manager.get_device_summary()
    print("Device summary: {}/{} devices available".format(summary['available'], summary['total']))
    
    print("=== Device Management Test Complete ===\n")

# Uncomment the line below to run device management tests
# test_device_management()

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

    device_manager.safe_device_call("pixy_camera", "light", False);

def lighton(value):
    #us_sensor.distance();

    """
    Perform the specified action.

    Args:
        value: The value to be used for the action.

    Returns:
        None
    """

    device_manager.safe_device_call("pixy_camera", "light", True);

def sayit(value):
    ev3.speaker.say("Hello, I am Wrack!")

def quit(value):
    value.stop()                                                  


def driftLeft(value):
    global robot_is_stopped
    tank_drive_system.drift_left(1000)
    robot_is_stopped = False

def driftRight(value):
    global robot_is_stopped
    tank_drive_system.drift_right(1000)
    robot_is_stopped = False


def driftStop(value):
    global robot_is_stopped
    tank_drive_system.stop()
    robot_is_stopped = True

def move(value): 
    """
    Moves the robot based on joystick input using the TankDriveSystem.

    Args:
        value: The joystick value containing l_left (steering) and l_forward (drive).

    Returns:
        None
    """
    # Use both steering (l_left) and drive (l_forward) inputs with proper deadzone filtering
    drive_speed = -1 * value.l_forward if abs(value.l_forward) >= MIN_JOYSTICK_MOVE else 0
    steer_input = value.l_left if abs(value.l_left) >= MIN_JOYSTICK_MOVE else 0
    
    # Only send commands if there's actual movement to reduce event flooding
    global robot_is_stopped
    
    if drive_speed != 0 or steer_input != 0:
        tank_drive_system.move_with_steering(drive_speed, steer_input)
        robot_is_stopped = False
    elif not robot_is_stopped:
        # Only stop once when joystick returns to rest to avoid redundant stop calls
        tank_drive_system.stop()
        robot_is_stopped = True

def watch(value):
    x=0; 
    """
    if (abs(value.r_left) < MIN_JOYSTICK_MOVE):
        turret_motor.stop();
    else:
        turret_motor.run(value.r_left)

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
    if not device_manager.is_device_available("pixy_camera"):
        return
        
    block = value.blocks[0];
    if(block.width > 10 or block.height > 10):
        scale_factor = block.x_center - 150;
        device_manager.safe_device_call("turret_motor", "run", scale_factor);




def main():
    """
    remoteController = RemoteController();
    remoteController.onFire(doit)
    remoteController.start()
    """
    controller = PS4Controller()

    # Only set up pixy camera event handler if camera is available
    if device_manager.is_device_available("pixy_camera"):
        pixy_camera.onBlockDetected(blockDetected);

    # Only set up light controls if pixy camera is available
    if device_manager.is_device_available("pixy_camera"):
        controller.onL1Button(lighton)
        controller.onR1Button(lightoff)
    
    #controller.onCrossButton(sayit)
    controller.onOptionsButton(quit)
    controller.onLeftJoystickMove(move)
    
    # Only set up drift controls if drive motors are available
    if device_manager.are_devices_available(["drive_L_motor", "drive_R_motor"]):
        controller.onLeftArrowPressed(driftLeft)
        controller.onRightArrowPressed(driftRight)
        controller.onLRArrowReleased(driftStop)
        
    controller.onRightJoystickMove(watch)
    controller.start()
    
    # Only start pixy camera if available
    if device_manager.is_device_available("pixy_camera"):
        pixy_camera.start()
        
    if __debug__:
        print ("Threads started")
    
    #Wait for controller thread to finish
    #controller.join()
    #pixy_camera.join();


main()
