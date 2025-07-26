from abc import ABC, abstractmethod
from typing import Optional, Tuple


class DriveSystem(ABC):
    """
    Abstract base class for robot drive systems.
    
    This class defines the interface that all drive system implementations
    must follow. It provides a standardized way to control robot movement
    regardless of the specific drive mechanism (tank drive, mecanum, etc.).
    """
    
    def __init__(self, device_manager=None):
        """
        Initialize the drive system.
        
        Args:
            device_manager: Optional DeviceManager instance for safe device operations
        """
        self.device_manager = device_manager
        self._is_initialized = False
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the drive system hardware.
        
        Returns:
            bool: True if initialization was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def move_forward(self, speed: int, duration: Optional[float] = None) -> None:
        """
        Move the robot forward.
        
        Args:
            speed: Speed value (implementation-specific range)
            duration: Optional duration in seconds. If None, move until stopped
        """
        pass
    
    @abstractmethod
    def move_backward(self, speed: int, duration: Optional[float] = None) -> None:
        """
        Move the robot backward.
        
        Args:
            speed: Speed value (implementation-specific range)
            duration: Optional duration in seconds. If None, move until stopped
        """
        pass
    
    @abstractmethod
    def turn_left(self, speed: int, duration: Optional[float] = None) -> None:
        """
        Turn the robot left.
        
        Args:
            speed: Speed value (implementation-specific range)
            duration: Optional duration in seconds. If None, turn until stopped
        """
        pass
    
    @abstractmethod
    def turn_right(self, speed: int, duration: Optional[float] = None) -> None:
        """
        Turn the robot right.
        
        Args:
            speed: Speed value (implementation-specific range)
            duration: Optional duration in seconds. If None, turn until stopped
        """
        pass
    
    @abstractmethod
    def move_with_steering(self, drive_speed: int, steer_angle: int) -> None:
        """
        Move with simultaneous drive and steering control.
        
        Args:
            drive_speed: Forward/backward speed
            steer_angle: Steering angle or turning speed
        """
        pass
    
    @abstractmethod
    def stop(self) -> None:
        """
        Stop all drive system movement immediately.
        """
        pass
    
    @abstractmethod
    def drift_left(self, speed: int) -> None:
        """
        Perform a left drift maneuver.
        
        Args:
            speed: Speed for the drift maneuver
        """
        pass
    
    @abstractmethod
    def drift_right(self, speed: int) -> None:
        """
        Perform a right drift maneuver.
        
        Args:
            speed: Speed for the drift maneuver
        """
        pass
    
    @abstractmethod
    def get_status(self) -> dict:
        """
        Get current status of the drive system.
        
        Returns:
            dict: Dictionary containing status information
        """
        pass
    
    def is_initialized(self) -> bool:
        """
        Check if the drive system is properly initialized.
        
        Returns:
            bool: True if initialized, False otherwise
        """
        return self._is_initialized
    
    def validate_speed(self, speed: int, min_speed: int = -1000, max_speed: int = 1000) -> int:
        """
        Validate and clamp speed values to acceptable range.
        
        Args:
            speed: Input speed value
            min_speed: Minimum allowed speed
            max_speed: Maximum allowed speed
            
        Returns:
            int: Clamped speed value
        """
        return max(min_speed, min(max_speed, speed))
    
    def safe_device_operation(self, device_name: str, operation_name: str, *args, **kwargs):
        """
        Safely perform an operation on a device through the device manager.
        
        Args:
            device_name: Name of the device
            operation_name: Name of the operation to perform
            *args: Positional arguments for the operation
            **kwargs: Keyword arguments for the operation
            
        Returns:
            Result of the operation or None if failed
        """
        if self.device_manager:
            return self.device_manager.safe_device_operation(
                device_name, operation_name, *args, **kwargs
            )
        return None
    
    def is_device_available(self, device_name: str) -> bool:
        """
        Check if a specific device is available.
        
        Args:
            device_name: Name of the device to check
            
        Returns:
            bool: True if device is available, False otherwise
        """
        if self.device_manager:
            return self.device_manager.is_device_available(device_name)
        return False 