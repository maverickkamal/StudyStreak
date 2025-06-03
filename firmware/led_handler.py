# -*- coding: utf-8 -*-
"""
WS2812B LED Handler for StudyStreak ESP32 Project
================================================

This module provides control for WS2812B RGB LEDs (NeoPixels) for visual feedback
in the Pomodoro timer. The handler supports individual LED control, color patterns,
breathing effects, and timer-specific visual states.

WS2812B LEDs are addressable RGB LEDs that can be controlled individually via
a single data line using precise timing protocols.

Author: StudyStreak Project
Version: 1.0
"""

import time


class LEDHandler:
    """
    Handler for WS2812B RGB LED strip control.
    
    This class provides conceptual interface for controlling WS2812B LEDs
    without actual hardware interaction. In a real implementation, this
    would use the neopixel library or similar for ESP32.
    """
    
    def __init__(self, pin, num_leds=8):
        """
        Initialize the LED handler.
        
        Args:
            pin (int): GPIO pin number for LED data line
            num_leds (int): Number of LEDs in the strip
        """
        self.pin = pin
        self.num_leds = num_leds
        self.is_initialized = False
        
        # LED state storage [R, G, B] for each LED
        self.led_states = [[0, 0, 0] for _ in range(num_leds)]
        
        # Animation variables
        self._breathing_phase = 0
        self._animation_running = False
        
        # Color definitions
        self.colors = {
            'off': (0, 0, 0),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'purple': (128, 0, 128),
            'orange': (255, 165, 0),
            'white': (255, 255, 255),
            'warm_white': (255, 180, 100),
            'cool_white': (200, 200, 255),
            'dim_red': (50, 0, 0),
            'dim_green': (0, 50, 0),
            'dim_blue': (0, 0, 50)
        }
        
        print(f"LEDHandler: Created for pin {self.pin} with {self.num_leds} LEDs")
    
    def setup(self):
        """
        Initialize the LED hardware.
        
        In a real implementation, this would:
        - Initialize the neopixel library
        - Configure the LED strip
        - Test initial LED states
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        print(f"Conceptual: Initializing WS2812B LEDs on pin {self.pin}")
        print(f"Conceptual: Configuring {self.num_leds} LEDs...")
        
        # Simulate initialization
        time.sleep(0.1)
        
        # Clear all LEDs
        self.clear_all()
        
        self.is_initialized = True
        print("Conceptual: LED strip initialized successfully")
        return True
    
    def set_led(self, led_index, color):
        """
        Set a specific LED to a color.
        
        Args:
            led_index (int): Index of the LED (0 to num_leds-1)
            color (tuple): RGB color tuple (r, g, b) with values 0-255
        """
        if not self.is_initialized:
            print("ERROR: LED handler not initialized! Call setup() first.")
            return False
        
        if not (0 <= led_index < self.num_leds):
            print(f"ERROR: LED index {led_index} out of range (0-{self.num_leds-1})")
            return False
        
        if not (isinstance(color, (tuple, list)) and len(color) == 3):
            print("ERROR: Color must be a tuple/list of 3 values (R, G, B)")
            return False
        
        # Validate color values
        r, g, b = color
        if not all(0 <= val <= 255 for val in [r, g, b]):
            print("ERROR: Color values must be between 0 and 255")
            return False
        
        # Store the color state
        self.led_states[led_index] = [r, g, b]
        
        print(f"Conceptual: LED {led_index} set to RGB({r}, {g}, {b})")
        return True
    
    def set_all_leds(self, color):
        """
        Set all LEDs to the same color.
        
        Args:
            color (tuple): RGB color tuple (r, g, b) with values 0-255
        """
        if not self.is_initialized:
            print("ERROR: LED handler not initialized! Call setup() first.")
            return False
        
        success = True
        for i in range(self.num_leds):
            if not self.set_led(i, color):
                success = False
        
        print(f"Conceptual: All LEDs set to RGB{color}")
        return success
    
    def clear_all(self):
        """
        Turn off all LEDs.
        """
        return self.set_all_leds(self.colors['off'])
    
    def update_display(self):
        """
        Update the physical LED display.
        
        In a real implementation, this would call the neopixel.write() method
        to actually update the LED strip with the current states.
        """
        if not self.is_initialized:
            print("ERROR: LED handler not initialized! Call setup() first.")
            return False
        
        print("Conceptual: Updating LED display...")
        for i, (r, g, b) in enumerate(self.led_states):
            if r > 0 or g > 0 or b > 0:  # Only print active LEDs
                print(f"  LED {i}: RGB({r}, {g}, {b})")
        
        return True
    
    def show_pomodoro_state(self, state, progress_percent=0):
        """
        Display visual feedback for current Pomodoro state.
        
        Args:
            state (str): Current timer state ('IDLE', 'WORK', 'BREAK_SHORT', 'BREAK_LONG')
            progress_percent (float): Progress percentage (0-100)
        """
        if not self.is_initialized:
            print("ERROR: LED handler not initialized! Call setup() first.")
            return
        
        print(f"LEDHandler: Showing state '{state}' with {progress_percent}% progress")
        
        if state == 'IDLE':
            # Dim white breathing effect
            self._breathing_effect(self.colors['dim_blue'], 0.5)
        
        elif state == 'WORK':
            # Red progress bar
            self._show_progress_bar(self.colors['red'], progress_percent)
        
        elif state == 'BREAK_SHORT':
            # Green progress bar
            self._show_progress_bar(self.colors['green'], progress_percent)
        
        elif state == 'BREAK_LONG':
            # Blue progress bar
            self._show_progress_bar(self.colors['blue'], progress_percent)
        
        else:
            print(f"Unknown state: {state}")
            self.clear_all()
        
        self.update_display()
    
    def _show_progress_bar(self, color, progress_percent):
        """
        Display a progress bar using the LED strip.
        
        Args:
            color (tuple): RGB color for the progress bar
            progress_percent (float): Progress percentage (0-100)
        """
        # Clear all LEDs first
        self.clear_all()
        
        # Calculate number of LEDs to light up
        num_lit = int((progress_percent / 100.0) * self.num_leds)
        
        # Light up the appropriate number of LEDs
        for i in range(num_lit):
            self.set_led(i, color)
        
        # Show partial progress on the next LED if applicable
        if num_lit < self.num_leds:
            partial_progress = ((progress_percent / 100.0) * self.num_leds) - num_lit
            if partial_progress > 0:
                # Dim the next LED based on partial progress
                r, g, b = color
                dimmed_color = (
                    int(r * partial_progress),
                    int(g * partial_progress),
                    int(b * partial_progress)
                )
                self.set_led(num_lit, dimmed_color)
    
    def _breathing_effect(self, base_color, intensity=1.0):
        """
        Create a breathing effect with the specified color.
        
        Args:
            base_color (tuple): Base RGB color
            intensity (float): Breathing intensity (0.0-1.0)
        """
        # Simple breathing calculation using phase
        import math
        breathing_factor = (math.sin(self._breathing_phase) + 1) / 2  # 0 to 1
        breathing_factor *= intensity
        
        r, g, b = base_color
        dimmed_color = (
            int(r * breathing_factor),
            int(g * breathing_factor),
            int(b * breathing_factor)
        )
        
        self.set_all_leds(dimmed_color)
        self._breathing_phase += 0.1
    
    def flash_notification(self, color, flash_count=3, duration=0.5):
        """
        Flash LEDs for notifications.
        
        Args:
            color (tuple): RGB color to flash
            flash_count (int): Number of flashes
            duration (float): Duration of each flash in seconds
        """
        if not self.is_initialized:
            print("ERROR: LED handler not initialized! Call setup() first.")
            return
        
        print(f"LEDHandler: Flashing {flash_count} times with color RGB{color}")
        
        for i in range(flash_count):
            # Flash on
            self.set_all_leds(color)
            self.update_display()
            time.sleep(duration / 2)
            
            # Flash off
            self.clear_all()
            self.update_display()
            time.sleep(duration / 2)
    
    def set_brightness(self, brightness):
        """
        Set global brightness for all LEDs.
        
        Args:
            brightness (float): Brightness level (0.0-1.0)
        """
        if not (0.0 <= brightness <= 1.0):
            print("ERROR: Brightness must be between 0.0 and 1.0")
            return False
        
        print(f"LEDHandler: Setting brightness to {brightness * 100}%")
        
        # Apply brightness to all current LED states
        for i in range(self.num_leds):
            r, g, b = self.led_states[i]
            self.led_states[i] = [
                int(r * brightness),
                int(g * brightness),
                int(b * brightness)
            ]
        
        return True
    
    def get_status(self):
        """
        Get current LED handler status.
        
        Returns:
            dict: Status information
        """
        return {
            'initialized': self.is_initialized,
            'pin': self.pin,
            'num_leds': self.num_leds,
            'led_states': self.led_states.copy(),
            'animation_running': self._animation_running
        }


# Example usage (commented out for module import)
"""
# Example of how to use the LEDHandler class

# Create LED handler for pin 5 with 8 LEDs
leds = LEDHandler(pin=5, num_leds=8)

# Initialize the LEDs
if leds.setup():
    print("LED setup successful!")
    
    # Test basic colors
    print("\n--- Testing basic colors ---")
    leds.set_all_leds(leds.colors['red'])
    leds.update_display()
    time.sleep(1)
    
    leds.set_all_leds(leds.colors['green'])
    leds.update_display()
    time.sleep(1)
    
    leds.set_all_leds(leds.colors['blue'])
    leds.update_display()
    time.sleep(1)
    
    # Test progress bar
    print("\n--- Testing progress bar ---")
    for progress in range(0, 101, 10):
        leds.show_pomodoro_state('WORK', progress)
        time.sleep(0.5)
    
    # Test flash notification
    print("\n--- Testing flash notification ---")
    leds.flash_notification(leds.colors['yellow'], flash_count=3)
    
    # Test different states
    print("\n--- Testing Pomodoro states ---")
    states = ['IDLE', 'WORK', 'BREAK_SHORT', 'BREAK_LONG']
    for state in states:
        print(f"Showing state: {state}")
        leds.show_pomodoro_state(state, 50)
        time.sleep(2)
    
    # Clear all LEDs
    leds.clear_all()
    leds.update_display()
    
    print("LED Status:", leds.get_status())

else:
    print("Failed to initialize LEDs!")
"""
