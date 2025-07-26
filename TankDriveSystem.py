from DriveSystem import DriveSystem
from typing import Optional
from time import sleep


class TankDriveSystem(DriveSystem):
    """
    Tank-style drive system implementation with independent left and right track motors.
    
    This implementation provides tank-like driving where steering is achieved through
    differential motor speeds between left and right tracks, rather than a separate
    steering mechanism.
    """
    
    def __init__(self, device_manager=None):
        """
        Initialize the tank drive system.
        
        Args:
            device_manager: DeviceManager instance for safe device operations
        """
        super().__init__(device_manager)
        self.left_motor_name = "drive_L_motor"
        self.right_motor_name = "drive_R_motor"
        
        # Default speeds
        self.default_drive_speed = 1000
        self.default_turn_speed = 500
        self.drift_speed = 1000
    
    def initialize(self) -> bool:
        """
        Initialize the tank drive system hardware.
        
        Returns:
            bool: True if initialization was successful, False otherwise
        """
        required_devices = [
            self.left_motor_name,
            self.right_motor_name
        ]
        
        available_devices = []
        for device in required_devices:
            if self.is_device_available(device):
                available_devices.append(device)
        
        # System is initialized if both motors are available
        self._is_initialized = len(available_devices) == 2
        
        if __debug__:
            print(f"TankDriveSystem initialized: {self._is_initialized}")
            print(f"Available devices: {available_devices}")
        
        return self._is_initialized
    
    def move_forward(self, speed: int, duration: Optional[float] = None) -> None:
        """
        Move the robot forward by running both tracks at the same speed.
        
        Args:
            speed: Speed value (-1000 to 1000)
            duration: Optional duration in seconds
        """
        validated_speed = self.validate_speed(speed)
        
        if self.is_device_available(self.left_motor_name):
            self.safe_device_operation(self.left_motor_name, "run", -validated_speed)
        
        if self.is_device_available(self.right_motor_name):
            self.safe_device_operation(self.right_motor_name, "run", -validated_speed)
        
        if duration:
            sleep(duration)
            self.stop()
    
    def move_backward(self, speed: int, duration: Optional[float] = None) -> None:
        """
        Move the robot backward by running both tracks in reverse.
        
        Args:
            speed: Speed value (-1000 to 1000)
            duration: Optional duration in seconds
        """
        validated_speed = self.validate_speed(speed)
        
        if self.is_device_available(self.left_motor_name):
            self.safe_device_operation(self.left_motor_name, "run", validated_speed)
        
        if self.is_device_available(self.right_motor_name):
            self.safe_device_operation(self.right_motor_name, "run", validated_speed)
        
        if duration:
            sleep(duration)
            self.stop()
    
    def turn_left(self, speed: int, duration: Optional[float] = None) -> None:
        """
        Turn the robot left by running right track faster than left track.
        
        Args:
            speed: Turning speed (-1000 to 1000)
            duration: Optional duration in seconds
        """
        validated_speed = self.validate_speed(speed)
        
        # For left turn: slow down or reverse left track, maintain right track
        left_speed = -validated_speed // 2  # Slower/reverse left track
        right_speed = -validated_speed      # Full speed right track
        
        if self.is_device_available(self.left_motor_name):
            self.safe_device_operation(self.left_motor_name, "run", left_speed)
        
        if self.is_device_available(self.right_motor_name):
            self.safe_device_operation(self.right_motor_name, "run", right_speed)
        
        if duration:
            sleep(duration)
            self.stop()
    
    def turn_right(self, speed: int, duration: Optional[float] = None) -> None:
        """
        Turn the robot right by running left track faster than right track.
        
        Args:
            speed: Turning speed (-1000 to 1000)
            duration: Optional duration in seconds
        """
        validated_speed = self.validate_speed(speed)
        
        # For right turn: maintain left track, slow down or reverse right track
        left_speed = -validated_speed       # Full speed left track
        right_speed = -validated_speed // 2 # Slower/reverse right track
        
        if self.is_device_available(self.left_motor_name):
            self.safe_device_operation(self.left_motor_name, "run", left_speed)
        
        if self.is_device_available(self.right_motor_name):
            self.safe_device_operation(self.right_motor_name, "run", right_speed)
        
        if duration:
            sleep(duration)
            self.stop()
    
    def move_with_steering(self, drive_speed: int, steer_angle: int) -> None:
        """
        Move with simultaneous drive and steering control using differential steering.
        
        Args:
            drive_speed: Forward/backward speed for both tracks
            steer_angle: Steering input (-1000 to 1000, negative = left, positive = right)
        """
        validated_drive_speed = self.validate_speed(drive_speed)
        validated_steer_angle = self.validate_speed(steer_angle)
        
        # Calculate differential steering
        # Base speed is the drive speed, then adjust each track based on steering
        base_speed = -validated_drive_speed  # Negative for forward direction
        
        # Steering adjustment: reduce one side's speed based on turn direction
        steer_factor = validated_steer_angle / 1000.0  # Normalize to -1.0 to 1.0
        
        # Calculate left and right motor speeds
        if steer_factor < 0:  # Turning left
            left_speed = int(base_speed * (1 + steer_factor))   # Reduce left speed
            right_speed = base_speed                            # Maintain right speed
        elif steer_factor > 0:  # Turning right
            left_speed = base_speed                             # Maintain left speed
            right_speed = int(base_speed * (1 - steer_factor))  # Reduce right speed
        else:  # Going straight
            left_speed = base_speed
            right_speed = base_speed
        
        # Apply speeds to motors
        if self.is_device_available(self.left_motor_name):
            self.safe_device_operation(self.left_motor_name, "run", left_speed)
        
        if self.is_device_available(self.right_motor_name):
            self.safe_device_operation(self.right_motor_name, "run", right_speed)
    
    def stop(self) -> None:
        """
        Stop all track movement immediately.
        """
        if self.is_device_available(self.left_motor_name):
            self.safe_device_operation(self.left_motor_name, "stop")
        
        if self.is_device_available(self.right_motor_name):
            self.safe_device_operation(self.right_motor_name, "stop")
    
    def drift_left(self, speed: int) -> None:
        """
        Perform a left drift by running tracks in opposite directions.
        
        Args:
            speed: Speed for the drift maneuver
        """
        validated_speed = self.validate_speed(speed, max_speed=self.drift_speed)
        
        # Left drift: left track backward, right track forward
        if self.is_device_available(self.left_motor_name):
            self.safe_device_operation(self.left_motor_name, "run", validated_speed)
        
        if self.is_device_available(self.right_motor_name):
            self.safe_device_operation(self.right_motor_name, "run", -validated_speed)
    
    def drift_right(self, speed: int) -> None:
        """
        Perform a right drift by running tracks in opposite directions.
        
        Args:
            speed: Speed for the drift maneuver
        """
        validated_speed = self.validate_speed(speed, max_speed=self.drift_speed)
        
        # Right drift: left track forward, right track backward
        if self.is_device_available(self.left_motor_name):
            self.safe_device_operation(self.left_motor_name, "run", -validated_speed)
        
        if self.is_device_available(self.right_motor_name):
            self.safe_device_operation(self.right_motor_name, "run", validated_speed)
    
    def get_status(self) -> dict:
        """
        Get current status of the tank drive system.
        
        Returns:
            dict: Dictionary containing status information
        """
        status = {
            "initialized": self._is_initialized,
            "devices": {
                "left_motor": self.is_device_available(self.left_motor_name),
                "right_motor": self.is_device_available(self.right_motor_name)
            },
            "drive_system_type": "tank_drive",
            "available_operations": []
        }
        
        # Determine available operations based on device availability
        if status["devices"]["left_motor"] and status["devices"]["right_motor"]:
            status["available_operations"].extend([
                "move_forward", "move_backward", "turn_left", "turn_right",
                "drift_left", "drift_right", "differential_steering"
            ])
        elif status["devices"]["left_motor"] or status["devices"]["right_motor"]:
            status["available_operations"].append("limited_movement")
        
        return status
    
    def pivot_left(self, speed: int, duration: Optional[float] = None) -> None:
        """
        Pivot left in place by running tracks in opposite directions.
        
        Args:
            speed: Pivot speed
            duration: Optional duration in seconds
        """
        validated_speed = self.validate_speed(speed)
        
        # Pivot left: left track backward, right track forward at same speed
        if self.is_device_available(self.left_motor_name):
            self.safe_device_operation(self.left_motor_name, "run", validated_speed)
        
        if self.is_device_available(self.right_motor_name):
            self.safe_device_operation(self.right_motor_name, "run", -validated_speed)
        
        if duration:
            sleep(duration)
            self.stop()
    
    def pivot_right(self, speed: int, duration: Optional[float] = None) -> None:
        """
        Pivot right in place by running tracks in opposite directions.
        
        Args:
            speed: Pivot speed
            duration: Optional duration in seconds
        """
        validated_speed = self.validate_speed(speed)
        
        # Pivot right: left track forward, right track backward at same speed
        if self.is_device_available(self.left_motor_name):
            self.safe_device_operation(self.left_motor_name, "run", -validated_speed)
        
        if self.is_device_available(self.right_motor_name):
            self.safe_device_operation(self.right_motor_name, "run", validated_speed)
        
        if duration:
            sleep(duration)
            self.stop()
    
    def set_motor_speeds(self, left_speed: int, right_speed: int) -> None:
        """
        Directly set individual motor speeds for advanced control.
        
        Args:
            left_speed: Speed for left track motor
            right_speed: Speed for right track motor
        """
        validated_left_speed = self.validate_speed(left_speed)
        validated_right_speed = self.validate_speed(right_speed)
        
        if self.is_device_available(self.left_motor_name):
            self.safe_device_operation(self.left_motor_name, "run", validated_left_speed)
        
        if self.is_device_available(self.right_motor_name):
            self.safe_device_operation(self.right_motor_name, "run", validated_right_speed)
    
    def set_default_speeds(self, drive_speed: int = None, turn_speed: int = None, drift_speed: int = None) -> None:
        """
        Set default speeds for various operations.
        
        Args:
            drive_speed: Default speed for forward/backward movement
            turn_speed: Default speed for turning operations
            drift_speed: Default speed for drift operations
        """
        if drive_speed is not None:
            self.default_drive_speed = self.validate_speed(drive_speed)
        
        if turn_speed is not None:
            self.default_turn_speed = self.validate_speed(turn_speed)
        
        if drift_speed is not None:
            self.drift_speed = self.validate_speed(drift_speed) 