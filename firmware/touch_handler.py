# -*- coding: utf-8 -*-
"""
Capacitive Touch Handler for StudyStreak ESP32 Project
=====================================================

This module provides control for capacitive touch sensors on ESP32 for user input
in the Pomodoro timer. The ESP32 has built-in capacitive touch sensors that can
detect touch through various materials.

Author: StudyStreak Project
Version: 1.0
"""

import time


class TouchHandler:
    """
    Handler for ESP32 capacitive touch sensors.
    
    This class provides conceptual interface for capacitive touch detection
    without actual hardware interaction. In a real implementation, this
    would use the ESP32's built-in touch sensor capabilities.
    """
    
    def __init__(self, touch_pins=None, threshold=500):
        """
        Initialize the touch handler.
        
        Args:
            touch_pins (list): List of touch-capable GPIO pins (T0-T9 on ESP32)
            threshold (int): Touch detection threshold (lower = more sensitive)
        """
        # Default touch pins if none provided (common ESP32 touch pins)
        if touch_pins is None:
            touch_pins = [4, 2, 15, 13, 12, 14, 27, 33, 32, 32]  # T0-T9
        
        self.touch_pins = touch_pins
        self.threshold = threshold
        self.is_initialized = False
        
        # Touch state tracking
        self.touch_states = {pin: False for pin in touch_pins}
        self.last_touch_time = {pin: 0 for pin in touch_pins}
        self.touch_callbacks = {}
        
        # Simulation variables
        self._simulation_mode = "idle"  # "idle", "touch", "cycle"
        self._simulation_pin = touch_pins[0] if touch_pins else 4
        self._cycle_counter = 0
        
        # Touch gesture detection
        self.long_press_duration = 1.0  # seconds
        self.double_tap_window = 0.5   # seconds
        self.debounce_time = 0.05      # seconds
        
        print(f"TouchHandler: Created with pins {self.touch_pins}")
        print(f"TouchHandler: Touch threshold set to {self.threshold}")
    
    def setup(self):
        """
        Initialize the touch sensors.
        
        In a real implementation, this would:
        - Initialize each touch pin
        - Set touch thresholds
        - Configure touch interrupts if needed
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        print("Conceptual: Initializing capacitive touch sensors...")
        
        for pin in self.touch_pins:
            print(f"Conceptual: Configuring touch pin T{pin}")
            print(f"Conceptual: Setting threshold to {self.threshold}")
        
        # Simulate initialization delay
        time.sleep(0.1)
        
        self.is_initialized = True
        print("Conceptual: Touch sensors initialized successfully")
        return True
    
    def read_touch_value(self, pin):
        """
        Read raw touch value from a specific pin.
        
        Args:
            pin (int): GPIO pin number to read
        
        Returns:
            int: Raw touch value (lower values indicate touch), or None if error
        """
        if not self.is_initialized:
            print("ERROR: Touch handler not initialized! Call setup() first.")
            return None
        
        if pin not in self.touch_pins:
            print(f"ERROR: Pin {pin} is not configured for touch sensing")
            return None
        
        # Simulate touch reading based on simulation mode
        if self._simulation_mode == "touch" and pin == self._simulation_pin:
            # Simulate touch detected (below threshold)
            touch_value = self.threshold - 100
        elif self._simulation_mode == "cycle":
            # Cycle through touch states
            if self._cycle_counter % 4 == 0 and pin == self._simulation_pin:
                touch_value = self.threshold - 150
            else:
                touch_value = self.threshold + 200
            self._cycle_counter += 1
        else:
            # Simulate no touch (above threshold)
            touch_value = self.threshold + 200
        
        # Add some noise for realism
        import random
        noise = random.randint(-20, 20)
        touch_value += noise
        
        # Ensure positive value
        touch_value = max(0, touch_value)
        
        print(f"Conceptual: Touch pin T{pin} raw value: {touch_value}")
        return touch_value
    
    def is_touched(self, pin):
        """
        Check if a specific pin is currently being touched.
        
        Args:
            pin (int): GPIO pin number to check
        
        Returns:
            bool: True if pin is touched, False otherwise
        """
        if not self.is_initialized:
            print("ERROR: Touch handler not initialized! Call setup() first.")
            return False
        
        touch_value = self.read_touch_value(pin)
        if touch_value is None:
            return False
        
        # Touch detected when value is below threshold
        is_touch = touch_value < self.threshold
        
        current_time = time.time()
        
        # Debounce logic
        if is_touch and not self.touch_states[pin]:
            if current_time - self.last_touch_time[pin] > self.debounce_time:
                self.touch_states[pin] = True
                self.last_touch_time[pin] = current_time
                print(f"Conceptual: Touch DETECTED on pin T{pin}")
                
                # Call callback if registered
                if pin in self.touch_callbacks:
                    self.touch_callbacks[pin]('press', pin)
                
                return True
        
        elif not is_touch and self.touch_states[pin]:
            self.touch_states[pin] = False
            print(f"Conceptual: Touch RELEASED on pin T{pin}")
            
            # Call callback if registered
            if pin in self.touch_callbacks:
                self.touch_callbacks[pin]('release', pin)
        
        return self.touch_states[pin]
    
    def scan_all_pins(self):
        """
        Scan all configured touch pins and return active touches.
        
        Returns:
            list: List of pins that are currently touched
        """
        if not self.is_initialized:
            print("ERROR: Touch handler not initialized! Call setup() first.")
            return []
        
        touched_pins = []
        for pin in self.touch_pins:
            if self.is_touched(pin):
                touched_pins.append(pin)
        
        return touched_pins
    
    def wait_for_touch(self, pin=None, timeout=None):
        """
        Wait for a touch event on a specific pin or any pin.
        
        Args:
            pin (int): Specific pin to wait for, or None for any pin
            timeout (float): Maximum time to wait in seconds, or None for no timeout
        
        Returns:
            int: Pin number that was touched, or None if timeout
        """
        if not self.is_initialized:
            print("ERROR: Touch handler not initialized! Call setup() first.")
            return None
        
        start_time = time.time()
        print(f"Conceptual: Waiting for touch on {'pin T' + str(pin) if pin else 'any pin'}...")
        
        while True:
            if pin is not None:
                # Wait for specific pin
                if self.is_touched(pin):
                    return pin
            else:
                # Wait for any pin
                touched_pins = self.scan_all_pins()
                if touched_pins:
                    return touched_pins[0]
            
            # Check timeout
            if timeout and (time.time() - start_time) > timeout:
                print("Conceptual: Touch wait timeout")
                return None
            
            time.sleep(0.01)  # Small delay to prevent busy waiting
    
    def detect_long_press(self, pin, duration=None):
        """
        Detect a long press on a specific pin.
        
        Args:
            pin (int): GPIO pin to monitor
            duration (float): Minimum press duration, or None for default
        
        Returns:
            bool: True if long press detected, False otherwise
        """
        if duration is None:
            duration = self.long_press_duration
        
        if not self.is_touched(pin):
            return False
        
        press_start = time.time()
        print(f"Conceptual: Monitoring for long press on pin T{pin}...")
        
        while self.is_touched(pin):
            if (time.time() - press_start) >= duration:
                print(f"Conceptual: Long press detected on pin T{pin} ({duration}s)")
                return True
            time.sleep(0.01)
        
        return False
    
    def detect_double_tap(self, pin, window=None):
        """
        Detect a double tap on a specific pin.
        
        Args:
            pin (int): GPIO pin to monitor
            window (float): Maximum time between taps, or None for default
        
        Returns:
            bool: True if double tap detected, False otherwise
        """
        if window is None:
            window = self.double_tap_window
        
        # Wait for first tap
        if not self.wait_for_touch(pin, timeout=0.1):
            return False
        
        # Wait for release
        while self.is_touched(pin):
            time.sleep(0.01)
        
        first_tap_time = time.time()
        
        # Wait for second tap within window
        while (time.time() - first_tap_time) < window:
            if self.is_touched(pin):
                print(f"Conceptual: Double tap detected on pin T{pin}")
                return True
            time.sleep(0.01)
        
        return False
    
    def register_callback(self, pin, callback_func):
        """
        Register a callback function for touch events on a pin.
        
        Args:
            pin (int): GPIO pin to monitor
            callback_func (callable): Function to call on touch events
                                    (event_type, pin) -> None
        """
        if pin not in self.touch_pins:
            print(f"ERROR: Pin {pin} is not configured for touch sensing")
            return False
        
        self.touch_callbacks[pin] = callback_func
        print(f"TouchHandler: Callback registered for pin T{pin}")
        return True
    
    def unregister_callback(self, pin):
        """
        Remove callback for a specific pin.
        
        Args:
            pin (int): GPIO pin to remove callback from
        """
        if pin in self.touch_callbacks:
            del self.touch_callbacks[pin]
            print(f"TouchHandler: Callback removed for pin T{pin}")
            return True
        return False
    
    def set_threshold(self, pin, threshold):
        """
        Set touch threshold for a specific pin.
        
        Args:
            pin (int): GPIO pin to configure
            threshold (int): New threshold value
        """
        if pin not in self.touch_pins:
            print(f"ERROR: Pin {pin} is not configured for touch sensing")
            return False
        
        # For simplicity, we use global threshold in this conceptual implementation
        self.threshold = threshold
        print(f"TouchHandler: Threshold for pin T{pin} set to {threshold}")
        return True
    
    def set_simulation_mode(self, mode, pin=None):
        """
        Set simulation mode for testing.
        
        Args:
            mode (str): "idle", "touch", or "cycle"
            pin (int): Pin to simulate touch on (optional)
        """
        if mode in ["idle", "touch", "cycle"]:
            self._simulation_mode = mode
            if pin is not None and pin in self.touch_pins:
                self._simulation_pin = pin
            print(f"TouchHandler: Simulation mode set to '{mode}' on pin T{self._simulation_pin}")
        else:
            print(f"ERROR: Invalid simulation mode '{mode}'. Use 'idle', 'touch', or 'cycle'")
    
    def calibrate_pin(self, pin, samples=10):
        """
        Calibrate touch threshold for a specific pin.
        
        Args:
            pin (int): GPIO pin to calibrate
            samples (int): Number of samples to take for calibration
        
        Returns:
            int: Suggested threshold value
        """
        if not self.is_initialized:
            print("ERROR: Touch handler not initialized! Call setup() first.")
            return None
        
        if pin not in self.touch_pins:
            print(f"ERROR: Pin {pin} is not configured for touch sensing")
            return None
        
        print(f"Conceptual: Calibrating pin T{pin} with {samples} samples...")
        print("Conceptual: Make sure pin is not being touched during calibration")
        
        readings = []
        for i in range(samples):
            value = self.read_touch_value(pin)
            if value is not None:
                readings.append(value)
            time.sleep(0.1)
        
        if readings:
            avg_value = sum(readings) / len(readings)
            suggested_threshold = int(avg_value * 0.8)  # 80% of untouched value
            
            print(f"Conceptual: Average untouched value: {avg_value:.1f}")
            print(f"Conceptual: Suggested threshold: {suggested_threshold}")
            
            return suggested_threshold
        
        return None
    
    def get_status(self):
        """
        Get current touch handler status.
        
        Returns:
            dict: Status information
        """
        return {
            'initialized': self.is_initialized,
            'touch_pins': self.touch_pins,
            'threshold': self.threshold,
            'touch_states': self.touch_states.copy(),
            'simulation_mode': self._simulation_mode,
            'simulation_pin': self._simulation_pin,
            'callbacks_registered': list(self.touch_callbacks.keys())
        }


# Example usage (commented out for module import)
"""
# Example of how to use the TouchHandler class

# Define touch callback function
def on_touch_event(event_type, pin):
    print(f"Touch callback: {event_type} on pin T{pin}")

# Create touch handler with default pins
touch = TouchHandler(touch_pins=[4, 2, 15], threshold=500)

# Initialize touch sensors
if touch.setup():
    print("Touch sensors setup successful!")
    
    # Register callback for pin 4
    touch.register_callback(4, on_touch_event)
    
    # Test different simulation modes
    print("\n--- Testing touch detection ---")
    
    modes = ["idle", "touch", "cycle"]
    for mode in modes:
        print(f"\nTesting mode: {mode}")
        touch.set_simulation_mode(mode, pin=4)
        
        # Check touch status
        for i in range(3):
            touched_pins = touch.scan_all_pins()
            if touched_pins:
                print(f"Touched pins: {touched_pins}")
            else:
                print("No touches detected")
            time.sleep(0.5)
    
    # Test gesture detection
    print("\n--- Testing gesture detection ---")
    touch.set_simulation_mode("touch", pin=4)
    
    # Test long press (simulated)
    print("Testing long press detection...")
    # In real implementation, this would wait for actual long press
    
    # Test calibration
    print("\n--- Testing calibration ---")
    touch.set_simulation_mode("idle", pin=4)
    suggested_threshold = touch.calibrate_pin(4, samples=5)
    print(f"Calibration result: {suggested_threshold}")
    
    # Show status
    print("\nTouch Handler Status:", touch.get_status())

else:
    print("Failed to initialize touch sensors!")
"""
