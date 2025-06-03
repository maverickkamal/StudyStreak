# -*- coding: utf-8 -*-
"""
SSD1306 OLED Display Handler for StudyStreak ESP32 Project
=========================================================

This module provides control for SSD1306 OLED displays for showing timer information,
progress, and status messages in the Pomodoro timer project.

The SSD1306 is a popular monochrome OLED display controller that supports I2C
and SPI communication protocols.

Author: StudyStreak Project
Version: 1.0
"""

import time


class OLEDHandler:
    """
    Handler for SSD1306 OLED display control.
    
    This class provides conceptual interface for controlling SSD1306 displays
    without actual hardware interaction. In a real implementation, this
    would use the ssd1306 library for MicroPython.
    """
    
    def __init__(self, width=128, height=64, i2c_address=0x3C):
        """
        Initialize the OLED handler.
        
        Args:
            width (int): Display width in pixels
            height (int): Display height in pixels
            i2c_address (int): I2C address of the display (typically 0x3C or 0x3D)
        """
        self.width = width
        self.height = height
        self.i2c_address = i2c_address
        self.is_initialized = False
        
        # Display buffer simulation
        self.display_buffer = []
        self.current_line = 0
        self.current_column = 0
        
        # Display settings
        self.contrast = 255
        self.is_inverted = False
        self.is_on = True
        
        print(f"OLEDHandler: Created for {width}x{height} display at I2C address 0x{i2c_address:02X}")
    
    def setup(self, i2c_sda_pin=21, i2c_scl_pin=22):
        """
        Initialize the OLED display.
        
        Args:
            i2c_sda_pin (int): GPIO pin for I2C SDA line
            i2c_scl_pin (int): GPIO pin for I2C SCL line
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        print(f"Conceptual: Initializing SSD1306 OLED display...")
        print(f"Conceptual: I2C SDA pin: {i2c_sda_pin}, SCL pin: {i2c_scl_pin}")
        print(f"Conceptual: Display resolution: {self.width}x{self.height}")
        print(f"Conceptual: I2C address: 0x{self.i2c_address:02X}")
        
        # Simulate initialization delay
        time.sleep(0.2)
        
        # Clear display buffer
        self.clear()
        
        self.is_initialized = True
        print("Conceptual: OLED display initialized successfully")
        return True
    
    def clear(self):
        """
        Clear the display buffer and screen.
        """
        if not self.is_initialized:
            print("ERROR: OLED display not initialized! Call setup() first.")
            return False
        
        self.display_buffer = []
        self.current_line = 0
        self.current_column = 0
        
        print("Conceptual: Display cleared")
        return True
    
    def show(self):
        """
        Update the physical display with the buffer contents.
        
        In a real implementation, this would call the display.show() method
        to push the buffer to the actual OLED display.
        """
        if not self.is_initialized:
            print("ERROR: OLED display not initialized! Call setup() first.")
            return False
        
        print("Conceptual: Updating OLED display...")
        print("=" * 32)
        
        # Display the buffer contents
        if self.display_buffer:
            for line in self.display_buffer:
                print(f"| {line:<30} |")
        else:
            print("|" + " " * 30 + "|")
        
        print("=" * 32)
        return True
    
    def print_line(self, text, line=None, center=False):
        """
        Print text on a specific line.
        
        Args:
            text (str): Text to display
            line (int): Line number (0-based), None for current line
            center (bool): Whether to center the text
        """
        if not self.is_initialized:
            print("ERROR: OLED display not initialized! Call setup() first.")
            return False
        
        if line is not None:
            self.current_line = line
        
        # Ensure we have enough lines in buffer
        while len(self.display_buffer) <= self.current_line:
            self.display_buffer.append("")
        
        # Format text
        display_text = str(text)
        if center and len(display_text) < 20:  # Assuming ~20 chars per line
            padding = (20 - len(display_text)) // 2
            display_text = " " * padding + display_text
        
        # Truncate if too long
        if len(display_text) > 20:
            display_text = display_text[:17] + "..."
        
        self.display_buffer[self.current_line] = display_text
        
        print(f"Conceptual: Line {self.current_line}: '{display_text}'")
        return True
    
    def print_centered(self, text, line=None):
        """
        Print centered text on a specific line.
        
        Args:
            text (str): Text to display
            line (int): Line number (0-based), None for current line
        """
        return self.print_line(text, line, center=True)
    
    def show_pomodoro_status(self, state, time_remaining, session_count=0):
        """
        Display current Pomodoro timer status.
        
        Args:
            state (str): Current timer state ('IDLE', 'WORK', 'BREAK_SHORT', 'BREAK_LONG')
            time_remaining (int): Remaining time in seconds
            session_count (int): Number of completed work sessions
        """
        if not self.is_initialized:
            print("ERROR: OLED display not initialized! Call setup() first.")
            return
        
        self.clear()
        
        # Format time as MM:SS
        minutes = time_remaining // 60
        seconds = time_remaining % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        
        # Display state-specific information
        if state == 'IDLE':
            self.print_centered("StudyStreak", 0)
            self.print_centered("Ready to Focus", 2)
            self.print_centered("Touch to Start", 4)
            if session_count > 0:
                self.print_centered(f"Sessions: {session_count}", 6)
        
        elif state == 'WORK':
            self.print_centered("FOCUS TIME", 0)
            self.print_centered(time_str, 2)
            self.show_progress_bar(time_remaining, 25 * 60, line=4)  # 25min work session
            if session_count > 0:
                self.print_centered(f"Session {session_count + 1}", 6)
        
        elif state == 'BREAK_SHORT':
            self.print_centered("SHORT BREAK", 0)
            self.print_centered(time_str, 2)
            self.show_progress_bar(time_remaining, 5 * 60, line=4)  # 5min break
            self.print_centered("Relax a bit!", 6)
        
        elif state == 'BREAK_LONG':
            self.print_centered("LONG BREAK", 0)
            self.print_centered(time_str, 2)
            self.show_progress_bar(time_remaining, 15 * 60, line=4)  # 15min break
            self.print_centered("Take a walk!", 6)
        
        elif state == 'PAUSED':
            self.print_centered("PAUSED", 0)
            self.print_centered(time_str, 2)
            self.print_centered("Touch to Resume", 4)
        
        self.show()
    
    def show_progress_bar(self, current_time, total_time, line=4, width=16):
        """
        Display a text-based progress bar.
        
        Args:
            current_time (int): Current/remaining time in seconds
            total_time (int): Total time for this phase in seconds
            line (int): Line number to display the progress bar
            width (int): Width of the progress bar in characters
        """
        if total_time <= 0:
            return
        
        # Calculate progress (inverted since current_time is remaining)
        progress = 1.0 - (current_time / total_time)
        progress = max(0.0, min(1.0, progress))
        
        # Create progress bar
        filled_chars = int(progress * width)
        bar = "█" * filled_chars + "░" * (width - filled_chars)
        
        # Display percentage
        percentage = int(progress * 100)
        bar_with_percent = f"{bar} {percentage:3d}%"
        
        self.print_line(bar_with_percent, line)
    
    def show_message(self, title, message, duration=None):
        """
        Display a message dialog.
        
        Args:
            title (str): Message title
            message (str): Message content
            duration (float): Optional auto-dismiss duration in seconds
        """
        if not self.is_initialized:
            print("ERROR: OLED display not initialized! Call setup() first.")
            return
        
        self.clear()
        self.print_centered(title, 1)
        self.print_centered("-" * len(title), 2)
        
        # Split message into lines if needed
        words = message.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= 20:
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Display message lines
        for i, line in enumerate(lines[:3]):  # Max 3 lines for message
            self.print_centered(line, 4 + i)
        
        self.show()
        
        if duration:
            print(f"Conceptual: Message will auto-dismiss in {duration} seconds")
            time.sleep(duration)
            self.clear()
            self.show()
    
    def show_notification(self, text, icon="!", duration=2.0):
        """
        Show a brief notification message.
        
        Args:
            text (str): Notification text
            icon (str): Icon character to display
            duration (float): Display duration in seconds
        """
        if not self.is_initialized:
            print("ERROR: OLED display not initialized! Call setup() first.")
            return
        
        self.clear()
        self.print_centered(f"[{icon}]", 1)
        self.print_centered(text, 3)
        self.show()
        
        if duration > 0:
            time.sleep(duration)
    
    def set_contrast(self, contrast):
        """
        Set display contrast.
        
        Args:
            contrast (int): Contrast value (0-255)
        """
        if not (0 <= contrast <= 255):
            print("ERROR: Contrast must be between 0 and 255")
            return False
        
        self.contrast = contrast
        print(f"Conceptual: Display contrast set to {contrast}")
        return True
    
    def set_invert(self, invert):
        """
        Set display inversion.
        
        Args:
            invert (bool): True to invert display, False for normal
        """
        self.is_inverted = invert
        print(f"Conceptual: Display inversion {'enabled' if invert else 'disabled'}")
        return True
    
    def display_on(self):
        """Turn the display on."""
        self.is_on = True
        print("Conceptual: Display turned ON")
        return True
    
    def display_off(self):
        """Turn the display off."""
        self.is_on = False
        print("Conceptual: Display turned OFF")
        return True
    
    def get_status(self):
        """
        Get current display status.
        
        Returns:
            dict: Status information
        """
        return {
            'initialized': self.is_initialized,
            'width': self.width,
            'height': self.height,
            'i2c_address': self.i2c_address,
            'contrast': self.contrast,
            'inverted': self.is_inverted,
            'display_on': self.is_on,
            'buffer_lines': len(self.display_buffer)
        }


# Example usage (commented out for module import)
"""
# Example of how to use the OLEDHandler class

# Create OLED handler for 128x64 display
oled = OLEDHandler(width=128, height=64, i2c_address=0x3C)

# Initialize the display
if oled.setup(i2c_sda_pin=21, i2c_scl_pin=22):
    print("OLED setup successful!")
    
    # Test basic text display
    print("\n--- Testing basic text display ---")
    oled.clear()
    oled.print_centered("StudyStreak", 0)
    oled.print_centered("Pomodoro Timer", 2)
    oled.show()
    time.sleep(2)
    
    # Test Pomodoro status display
    print("\n--- Testing Pomodoro status display ---")
    states = [
        ('IDLE', 0, 0),
        ('WORK', 1500, 1),  # 25 minutes remaining, session 1
        ('BREAK_SHORT', 300, 1),  # 5 minutes remaining
        ('BREAK_LONG', 900, 2)   # 15 minutes remaining, after session 2
    ]
    
    for state, time_remaining, session_count in states:
        print(f"Showing state: {state}")
        oled.show_pomodoro_status(state, time_remaining, session_count)
        time.sleep(3)
    
    # Test message display
    print("\n--- Testing message display ---")
    oled.show_message("Timer Complete!", "Great job! Take a well-deserved break.", duration=3)
    
    # Test notification
    print("\n--- Testing notification ---")
    oled.show_notification("Session Started", "▶", duration=2)
    
    # Test display controls
    print("\n--- Testing display controls ---")
    oled.set_contrast(128)
    oled.set_invert(True)
    time.sleep(1)
    oled.set_invert(False)
    
    # Clear display
    oled.clear()
    oled.show()
    
    print("OLED Status:", oled.get_status())

else:
    print("Failed to initialize OLED display!")
"""
