class DeviceManager:
    """
    Manages device initialization and provides safe access to devices.
    Handles missing devices gracefully by providing dummy objects.
    """
    
    def __init__(self):
        self.devices = {}
        self.available_devices = []
        self.missing_devices = []
        
    def try_init_device(self, device_type, port, device_name):
        """
        Try to initialize a device on a specific port.
        Returns the device if successful, None if failed.
        """
        try:
            device = device_type(port)
            self.devices[device_name] = device
            self.available_devices.append(device_name)
            if __debug__:
                print("✓ {} initialized on {}".format(device_name, port))
            return device
        except Exception as e:
            self.devices[device_name] = None
            self.missing_devices.append(device_name)
            if __debug__:
                print("✗ {} not found on {}: {}".format(device_name, port, e))
            return None
    
    def init_device_with_fallback(self, device_type, port, device_name, fallback_device=None):
        """
        Initialize a device with an optional fallback device.
        If the main device fails, it will try to use the fallback device.
        """
        device = self.try_init_device(device_type, port, device_name)
        if device is None and fallback_device is not None:
            if __debug__:
                print("Using fallback device for {}".format(device_name))
            self.devices[device_name] = fallback_device
            self.available_devices.append(device_name)
            return fallback_device
        return device
    
    def get_device(self, device_name):
        """
        Get a device safely. Returns the device or None if not available.
        """
        return self.devices.get(device_name)
    
    def is_device_available(self, device_name):
        """
        Check if a device is available.
        """
        return self.devices.get(device_name) is not None
    
    def are_devices_available(self, device_names):
        """
        Check if multiple devices are available.
        Returns True only if ALL specified devices are available.
        """
        return all(self.is_device_available(name) for name in device_names)
    
    def safe_device_call(self, device_name, method_name, *args, **kwargs):
        """
        Safely call a method on a device if it exists.
        """
        device = self.get_device(device_name)
        if device is not None:
            method = getattr(device, method_name, None)
            if method:
                return method(*args, **kwargs)
        return None
    
    def safe_device_operation(self, device_name, operation_name, operation_func, *args, **kwargs):
        """
        Safely perform an operation on a device with custom error handling.
        
        Args:
            device_name: Name of the device
            operation_name: Name of the operation for logging
            operation_func: Function to call on the device
            *args, **kwargs: Arguments to pass to the operation function
        """
        device = self.get_device(device_name)
        if device is not None:
            try:
                return operation_func(device, *args, **kwargs)
            except Exception as e:
                if __debug__:
                    print("Error in {} on {}: {}".format(operation_name, device_name, e))
                return None
        else:
            if __debug__:
                print("Cannot perform {} - {} not available".format(operation_name, device_name))
            return None
    
    def print_device_status(self):
        """
        Print the status of all devices.
        """
        print("\n=== Device Status ===")
        if self.available_devices:
            print("Available devices:")
            for device in self.available_devices:
                print("  ✓ {}".format(device))
        
        if self.missing_devices:
            print("Missing devices:")
            for device in self.missing_devices:
                print("  ✗ {}".format(device))
        print("==================\n")
    
    def get_device_summary(self):
        """
        Get a summary of device status.
        """
        total_devices = len(self.devices)
        available_count = len(self.available_devices)
        missing_count = len(self.missing_devices)
        
        return {
            'total': total_devices,
            'available': available_count,
            'missing': missing_count,
            'available_devices': self.available_devices.copy(),
            'missing_devices': self.missing_devices.copy()
        }