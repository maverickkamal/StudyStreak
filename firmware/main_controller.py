"""
StudyStreak Main Controller
==========================

This is the main application orchestrator for the ESP32-based StudyStreak project.
It manages the integration between the Pomodoro timer logic and future hardware handlers.

Author: StudyStreak Project
Environment: MicroPython for ESP32
"""

import utime
from pomodoro_logic import PomodoroTimer, STATE_IDLE, STATE_WORK, STATE_BREAK_SHORT
from led_handler import LEDHandler
from oled_handler import OLEDHandler
from touch_handler import TouchHandler
from tcrts5000_handler import PresenceSensor

# Configuration constants
MAIN_LOOP_DELAY_MS = 200  # Main loop delay to prevent excessive CPU usage
TOUCH_DEBOUNCE_MS = 300   # Debounce time for touch inputs

class StudyStreakController:
    """
    Main application controller that orchestrates all StudyStreak components.
    """
    
    def __init__(self):
        """
        Initialize the StudyStreak controller and all subsystems.
        """
        print("🚀 Initializing StudyStreak Controller...")
        
        # Initialize Pomodoro timer (core logic)
        self.pomodoro_timer = PomodoroTimer(work_mins=25, break_mins=5)
        print("✅ Pomodoro timer initialized")
        
        # Initialize hardware handlers
        try:
            # RGB LED control (WS2812B)
            self.led_handler = LEDHandler(pin=5, num_leds=8)
            self.led_handler.setup()
            print("✅ LED handler initialized")
            
            # OLED display management (SSD1306)
            self.oled_handler = OLEDHandler(width=128, height=64, i2c_address=0x3C)
            self.oled_handler.setup(i2c_sda_pin=21, i2c_scl_pin=22)
            print("✅ OLED handler initialized")
            
            # Capacitive touch input
            self.touch_handler = TouchHandler(touch_pins=[4, 2, 15], threshold=500)
            self.touch_handler.setup()
            self.touch_handler.register_callback(4, self._on_touch_event)
            print("✅ Touch handler initialized")
            
            # Presence sensor (TCRT5000)
            self.presence_sensor = PresenceSensor(conceptual_adc_pin=34, threshold=2500)
            self.presence_sensor.setup_sensor()
            print("✅ Presence sensor initialized")
            
            print("✅ All hardware handlers initialized")
            
        except Exception as e:
            print(f"⚠️  Hardware initialization error: {e}")
            print("🔄 Running in simulation mode")
        
        # State tracking for input debouncing and system status
        self.last_touch_time_ms = 0
        self.last_state = STATE_IDLE
        self.presence_detected = True  # Assume present initially
          # Display welcome message
        self._show_welcome_message()
        
        print("🎯 StudyStreak Controller ready!")
    
    def _on_touch_event(self, event_type, pin):
        """
        Callback function for touch events.
        
        Args:
            event_type (str): 'press' or 'release'
            pin (int): Touch pin that triggered the event
        """
        if event_type == 'press':
            current_time_ms = utime.ticks_ms()
            
            # Debounce touch input
            if utime.ticks_diff(current_time_ms, self.last_touch_time_ms) < TOUCH_DEBOUNCE_MS:
                return
            
            self.last_touch_time_ms = current_time_ms
            
            # Touch action logic based on current state
            if self.pomodoro_timer.get_state() == STATE_IDLE:
                print("👆 Touch detected: Starting work session")
                self.pomodoro_timer.start_work()
                self.oled_handler.show_notification("Session Started", "▶", duration=1.5)
                self.led_handler.flash_notification(self.led_handler.colors['green'], flash_count=2)
            elif self.pomodoro_timer.is_timer_paused():
                print("👆 Touch detected: Resuming timer")
                self.pomodoro_timer.resume()
                self.oled_handler.show_notification("Timer Resumed", "▶", duration=1.5)
            else:
                print("👆 Touch detected: Pausing timer")
                self.pomodoro_timer.pause()
                self.oled_handler.show_notification("Timer Paused", "⏸", duration=1.5)
    
    def _show_welcome_message(self):
        """
        Display welcome message on OLED and LED startup sequence.
        """
        try:
            # Show welcome on OLED
            self.oled_handler.clear()
            self.oled_handler.print_centered("StudyStreak", 1)
            self.oled_handler.print_centered("Pomodoro Timer", 3)
            self.oled_handler.print_centered("Touch to Start", 5)
            self.oled_handler.show()
            
            # LED startup sequence
            colors = ['red', 'green', 'blue', 'off']
            for color in colors:
                self.led_handler.set_all_leds(self.led_handler.colors[color])
                self.led_handler.update_display()
                utime.sleep_ms(200)
            
        except Exception as e:
            print(f"Welcome message error: {e}")
    
    def handle_touch_input(self):
        """
        Process touch input to control the Pomodoro timer.
        """
        try:
            # Touch input is now handled via callbacks in _on_touch_event
            # This method can be used for additional touch processing if needed
            touched_pins = self.touch_handler.scan_all_pins()
              # Handle long press for reset functionality
            if touched_pins and 4 in touched_pins:
                if self.touch_handler.detect_long_press(4, duration=3.0):
                    print("🔄 Long press detected: Resetting timer")
                    self.pomodoro_timer.reset()
                    self.oled_handler.show_notification("Timer Reset", "🔄", duration=2.0)
                    self.led_handler.flash_notification(self.led_handler.colors['purple'], flash_count=3)
                    
        except Exception as e:
            print(f"Touch input error: {e}")
    def handle_presence_sensor(self):
        """
        Process presence sensor data to automatically pause/resume timer.
        """
        try:
            # Read current presence status
            current_presence = self.presence_sensor.is_present()
            
            # Check for presence state change
            if current_presence != self.presence_detected:
                self.presence_detected = current_presence
                
                # Only auto-pause/resume during active timer states
                if self.pomodoro_timer.get_state() != STATE_IDLE:
                    if not self.presence_detected:
                        print("👤 Presence lost: Auto-pausing timer")
                        self.pomodoro_timer.pause()
                        self.oled_handler.show_notification("Auto-Paused", "👤", duration=2.0)
                        self.led_handler.set_all_leds(self.led_handler.colors['orange'])
                        self.led_handler.update_display()
                    elif self.pomodoro_timer.is_timer_paused():
                        print("👤 Presence detected: Auto-resuming timer")
                        self.pomodoro_timer.resume()
                        self.oled_handler.show_notification("Auto-Resumed", "👤", duration=2.0)
                        
        except Exception as e:
            print(f"Presence sensor error: {e}")    
    
    def update_display(self, current_state, time_str, progress_percent):
        """
        Update the OLED display with current timer information.
        """
        try:
            # Get session count for display
            session_count = getattr(self.pomodoro_timer, 'session_count', 0)
            
            # Convert time string to seconds for display handler
            time_parts = time_str.split(':')
            if len(time_parts) == 2:
                minutes, seconds = map(int, time_parts)
                time_remaining_seconds = minutes * 60 + seconds
            else:
                time_remaining_seconds = 0
            
            # Convert numeric state to string for display handler
            state_name = self.pomodoro_timer.get_state_name()
            
            # Update display based on current state
            self.oled_handler.show_pomodoro_status(
                state_name, 
                time_remaining_seconds, 
                session_count
            )
        except Exception as e:
            print(f"Display update error: {e}")
    
    def update_led_indicator(self, current_state):
        """
        Update RGB LED color and effects based on current Pomodoro state.
        """
        try:
            # Get progress for LED effects
            progress_percent = self.pomodoro_timer.get_session_progress_percent()
            
            # Convert numeric state to string for LED handler
            state_name = self.pomodoro_timer.get_state_name()
            
            # Update LEDs based on state
            self.led_handler.show_pomodoro_state(state_name, progress_percent)
            
        except Exception as e:
            print(f"LED update error: {e}")
    def handle_state_transitions(self, current_state):
        """
        Handle actions when timer state changes (work -> break, etc.).
        """
        if current_state != self.last_state:
            print(f"🔄 State transition: {self.pomodoro_timer.get_state_name()}")
            
            try:
                # Trigger notification effects based on state transitions
                if current_state == STATE_BREAK_SHORT:
                    print("🎉 Work session completed! Break time!")
                    self.led_handler.flash_notification(
                        self.led_handler.colors['green'], 
                        flash_count=3, 
                        duration=0.3
                    )
                    self.oled_handler.show_message(
                        "Work Complete!", 
                        "Time for a break! You earned it.", 
                        duration=3.0
                    )
                    
                elif current_state == STATE_WORK and self.last_state == STATE_BREAK_SHORT:
                    print("💪 Break completed! Back to work!")
                    self.led_handler.flash_notification(
                        self.led_handler.colors['red'], 
                        flash_count=3, 
                        duration=0.3
                    )
                    self.oled_handler.show_message(
                        "Break Over!", 
                        "Ready to focus again? Let's go!", 
                        duration=3.0
                    )
                    
                elif current_state == STATE_IDLE:
                    print("✅ Timer session completed!")
                    self.led_handler.flash_notification(
                        self.led_handler.colors['blue'], 
                        flash_count=5, 
                        duration=0.2
                    )
                    # Get session count for completion message
                    session_count = getattr(self.pomodoro_timer, 'session_count', 0)
                    self.oled_handler.show_message(
                        "Session Complete!", 
                        f"Completed {session_count} sessions. Great work!", 
                        duration=4.0
                    )
                
            except Exception as e:
                print(f"State transition effect error: {e}")
            
            self.last_state = current_state
    
    def run(self):
        """
        Main application loop.
        """
        print("🏃 Starting StudyStreak main loop...")
        
        try:
            while True:
                # Update core Pomodoro timer logic
                self.pomodoro_timer.update()
                
                # Get current timer information
                current_state = self.pomodoro_timer.get_state()
                time_str = self.pomodoro_timer.get_remaining_time_str()
                progress_percent = self.pomodoro_timer.get_session_progress_percent()
                
                # Handle input processing
                self.handle_touch_input()
                self.handle_presence_sensor()
                
                # Handle state change notifications
                self.handle_state_transitions(current_state)
                
                # Update output devices
                self.update_display(current_state, time_str, progress_percent)
                self.update_led_indicator(current_state)
                
                # Debug output (remove in production)
                if current_state != STATE_IDLE:
                    state_name = self.pomodoro_timer.get_state_name()
                    pause_indicator = " [PAUSED]" if self.pomodoro_timer.is_timer_paused() else ""
                    print(f"📊 {state_name}: {time_str} ({progress_percent:.1f}%){pause_indicator}")
                
                # Main loop delay to prevent excessive CPU usage
                utime.sleep_ms(MAIN_LOOP_DELAY_MS)
                
        except KeyboardInterrupt:
            print("\n🛑 StudyStreak stopped by user")
        except Exception as e:
            print(f"❌ StudyStreak error: {e}")
            # TODO: Log error and attempt graceful recovery
        finally:
            # TODO: Cleanup hardware resources
            # self.led_handler.cleanup()
            # self.oled_handler.cleanup()
            # self.touch_handler.cleanup()
            # self.sensor_handler.cleanup()
            print("🔌 StudyStreak controller shutdown complete")

def main():
    """
    Application entry point.
    """
    print("=" * 50)
    print("🎓 StudyStreak ESP32 Pomodoro Timer")
    print("=" * 50)
    
    # Create and run the main controller
    controller = StudyStreakController()
    controller.run()

# Entry point for MicroPython
if __name__ == "__main__":
    main()
