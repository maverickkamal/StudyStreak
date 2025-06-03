# -*- coding: utf-8 -*-
"""
TCRT5000 Presence Sensor Handler for StudyStreak ESP32 Project
=============================================================

This module provides a conceptual interface for interacting with a TCRT5000
reflective optical sensor for presence detection. This is an "offline" simulation
version that defines the logic and interface without actual hardware interaction.

The TCRT5000 is an infrared reflective sensor that can detect the presence of
objects by measuring reflected IR light. Higher ADC readings typically indicate
closer objects or better reflection.

Author: StudyStreak Project
Version: 1.0
"""

import time


class PresenceSensor:
    """
    Conceptual handler for TCRT5000 reflective optical sensor.
    
    This class simulates the interface and logic for presence detection
    without actual hardware interaction. In a real implementation, this
    would interface with an ESP32's ADC pin to read sensor values.
    """
    
    def __init__(self, conceptual_adc_pin, threshold=2500):
        """
        Initialize the presence sensor handler.
        
        Args:
            conceptual_adc_pin (int): GPIO pin number the sensor would be connected to
            threshold (int): ADC reading threshold above which presence is detected
                           (typical ESP32 ADC range: 0-4095 for 12-bit resolution)
        """
        self.adc_pin_number = conceptual_adc_pin
        self.presence_threshold = threshold
        self.is_initialized = False
        
        # Simulation variables for testing
        self._simulation_mode = "presence"  # "presence", "no_presence", or "cycle"
        self._cycle_counter = 0
        
        print(f"PresenceSensor: Created for conceptual ADC pin {self.adc_pin_number}")
        print(f"PresenceSensor: Presence threshold set to {self.presence_threshold}")
    
    def setup_sensor(self):
        """
        Initialize the TCRT5000 sensor (conceptual).
        
        In a real implementation, this would:
        - Initialize the ADC pin
        - Configure ADC parameters (attenuation, width)
        - Perform initial calibration if needed
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        print(f"Conceptual: Initializing TCRT5000 on ADC pin {self.adc_pin_number}")
        print("Conceptual: Configuring ADC parameters...")
        print("Conceptual: Performing sensor warm-up...")
        
        # Simulate initialization delay
        time.sleep(0.1)
        
        self.is_initialized = True
        print("Conceptual: TCRT5000 sensor initialized successfully")
        return True
    
    def read_raw_value(self):
        """
        Read raw ADC value from TCRT5000 sensor (conceptual).
        
        In a real implementation, this would read the analog value
        from the ESP32's ADC pin connected to the sensor's AO output.
        
        Returns:
            int: Raw ADC reading (0-4095 for ESP32 12-bit ADC), or None if error
        """
        if not self.is_initialized:
            print("ERROR: TCRT5000 sensor not initialized! Call setup_sensor() first.")
            return None
        
        print("Conceptual: Reading raw value from TCRT5000...")
        
        # Simulate different sensor readings based on simulation mode
        if self._simulation_mode == "presence":
            # Simulate presence detected (above threshold)
            raw_value = self.presence_threshold + 500
        elif self._simulation_mode == "no_presence":
            # Simulate no presence (below threshold)
            raw_value = self.presence_threshold - 500
        else:  # cycle mode
            # Alternate between presence and no presence for testing
            if self._cycle_counter % 2 == 0:
                raw_value = self.presence_threshold + 300
            else:
                raw_value = self.presence_threshold - 300
            self._cycle_counter += 1
        
        # Add some realistic noise to the reading
        import random
        noise = random.randint(-50, 50)
        raw_value += noise
        
        # Ensure value stays within valid ADC range
        raw_value = max(0, min(4095, raw_value))
        
        print(f"Conceptual: Raw ADC reading = {raw_value}")
        return raw_value
    
    def is_present(self):
        """
        Determine if presence is detected based on sensor reading.
        
        Returns:
            bool: True if presence detected, False otherwise
        """
        if not self.is_initialized:
            print("ERROR: TCRT5000 sensor not initialized! Call setup_sensor() first.")
            return False
        
        raw_value = self.read_raw_value()
        
        if raw_value is None:
            print("ERROR: Failed to read sensor value")
            return False
        
        # Compare against threshold to determine presence
        presence_detected = raw_value > self.presence_threshold
        
        print(f"Conceptual: Raw value {raw_value} vs threshold {self.presence_threshold}")
        if presence_detected:
            print("Conceptual: PRESENCE DETECTED")
        else:
            print("Conceptual: No presence detected")
        
        return presence_detected
    
    def set_simulation_mode(self, mode):
        """
        Set the simulation mode for testing purposes.
        
        Args:
            mode (str): "presence", "no_presence", or "cycle"
        """
        if mode in ["presence", "no_presence", "cycle"]:
            self._simulation_mode = mode
            print(f"PresenceSensor: Simulation mode set to '{mode}'")
        else:
            print(f"ERROR: Invalid simulation mode '{mode}'. Use 'presence', 'no_presence', or 'cycle'")
    
    def get_threshold(self):
        """
        Get the current presence detection threshold.
        
        Returns:
            int: Current threshold value
        """
        return self.presence_threshold
    
    def set_threshold(self, new_threshold):
        """
        Update the presence detection threshold.
        
        Args:
            new_threshold (int): New threshold value (0-4095)
        """
        if 0 <= new_threshold <= 4095:
            self.presence_threshold = new_threshold
            print(f"PresenceSensor: Threshold updated to {new_threshold}")
        else:
            print("ERROR: Threshold must be between 0 and 4095")
    
    def get_status(self):
        """
        Get current sensor status information.
        
        Returns:
            dict: Status information including initialization state, pin, threshold
        """
        return {
            'initialized': self.is_initialized,
            'adc_pin': self.adc_pin_number,
            'threshold': self.presence_threshold,
            'simulation_mode': self._simulation_mode
        }


# Example usage (commented out for module import)
"""
# Example of how to use the PresenceSensor class

# Create sensor instance for ADC pin 34 with default threshold
sensor = PresenceSensor(conceptual_adc_pin=34, threshold=2500)

# Initialize the sensor
if sensor.setup_sensor():
    print("Sensor setup successful!")
    
    # Test different simulation modes
    for mode in ["presence", "no_presence", "cycle"]:
        print(f"\n--- Testing {mode} mode ---")
        sensor.set_simulation_mode(mode)
        
        # Take several readings
        for i in range(3):
            print(f"Reading {i+1}:")
            present = sensor.is_present()
            print(f"Presence detected: {present}")
            time.sleep(0.5)
    
    # Check sensor status
    print("\nSensor Status:", sensor.get_status())
    
    # Update threshold
    sensor.set_threshold(3000)
    print("Testing with new threshold...")
    present = sensor.is_present()
    print(f"Presence detected: {present}")

else:
    print("Failed to initialize sensor!")
"""
