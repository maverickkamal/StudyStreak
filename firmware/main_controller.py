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
        self.pomodoro_timer = PomodoroTimer(work_mins=45, break_mins=5)
        print("✅ Pomodoro timer initialized")
        
        # TODO: Initialize hardware handlers (placeholders for future implementation)
        # self.led_handler = LEDHandler()           # RGB LED control
        # self.oled_handler = OLEDHandler()         # OLED display management
        # self.touch_handler = TouchHandler()       # Capacitive touch input
        # self.sensor_handler = SensorHandler()     # Presence/motion sensor
        # print("✅ Hardware handlers initialized")
        
        # State tracking for input debouncing and system status
        self.last_touch_time_ms = 0
        self.last_state = STATE_IDLE
        self.presence_detected = True  # Assume present initially
        
        print("🎯 StudyStreak Controller ready!")
    
    def handle_touch_input(self):
        """
        Process touch input to control the Pomodoro timer.
        This is a placeholder for future touch handler integration.
        """
        # TODO: Read touch input from touch_handler
        # touch_detected = self.touch_handler.is_touched()
        
        # Debounce touch input to prevent multiple triggers
        current_time_ms = utime.ticks_ms()
        if utime.ticks_diff(current_time_ms, self.last_touch_time_ms) < TOUCH_DEBOUNCE_MS:
            return
        
        # TODO: Implement actual touch detection
        # if touch_detected:
        #     self.last_touch_time_ms = current_time_ms
        #     
        #     # Touch action logic based on current state
        #     if self.pomodoro_timer.get_state() == STATE_IDLE:
        #         print("👆 Touch detected: Starting work session")
        #         self.pomodoro_timer.start_work()
        #     elif self.pomodoro_timer.is_timer_paused():
        #         print("👆 Touch detected: Resuming timer")
        #         self.pomodoro_timer.resume()
        #     else:
        #         print("👆 Touch detected: Pausing timer")
        #         self.pomodoro_timer.pause()
    
    def handle_presence_sensor(self):
        """
        Process presence sensor data to automatically pause/resume timer.
        This is a placeholder for future sensor handler integration.
        """
        # TODO: Read presence sensor from sensor_handler
        # current_presence = self.sensor_handler.is_presence_detected()
        
        # TODO: Implement presence-based timer control
        # if current_presence != self.presence_detected:
        #     self.presence_detected = current_presence
        #     
        #     if self.pomodoro_timer.get_state() != STATE_IDLE:
        #         if not self.presence_detected:
        #             print("👤 Presence lost: Auto-pausing timer")
        #             self.pomodoro_timer.pause()
        #         elif self.pomodoro_timer.is_timer_paused():
        #             print("👤 Presence detected: Auto-resuming timer")
        #             self.pomodoro_timer.resume()
    
    def update_display(self, current_state, time_str, progress_percent):
        """
        Update the OLED display with current timer information.
        This is a placeholder for future OLED handler integration.
        """
        # TODO: Update OLED display using oled_handler
        # self.oled_handler.clear_display()
        # 
        # # Display current state
        # state_name = self.pomodoro_timer.get_state_name()
        # self.oled_handler.draw_text(0, 0, f"State: {state_name}", font_size=12)
        # 
        # # Display remaining time
        # self.oled_handler.draw_text(0, 16, f"Time: {time_str}", font_size=16)
        # 
        # # Display progress bar
        # self.oled_handler.draw_progress_bar(0, 32, 128, 8, progress_percent)
        # 
        # # Display pause indicator if paused
        # if self.pomodoro_timer.is_timer_paused():
        #     self.oled_handler.draw_text(0, 48, "PAUSED", font_size=12)
        # 
        # self.oled_handler.show()
        pass
    
    def update_led_indicator(self, current_state):
        """
        Update RGB LED color based on current Pomodoro state.
        This is a placeholder for future LED handler integration.
        """
        # TODO: Set RGB LED color based on current_state using led_handler
        # if current_state == STATE_IDLE:
        #     self.led_handler.set_color(0, 0, 255)      # Blue for idle
        # elif current_state == STATE_WORK:
        #     if self.pomodoro_timer.is_timer_paused():
        #         self.led_handler.set_color(255, 165, 0)  # Orange for paused work
        #     else:
        #         self.led_handler.set_color(255, 0, 0)    # Red for active work
        # elif current_state == STATE_BREAK_SHORT:
        #     if self.pomodoro_timer.is_timer_paused():
        #         self.led_handler.set_color(255, 255, 0)  # Yellow for paused break
        #     else:
        #         self.led_handler.set_color(0, 255, 0)    # Green for active break
        pass
    
    def handle_state_transitions(self, current_state):
        """
        Handle actions when timer state changes (work -> break, etc.).
        """
        if current_state != self.last_state:
            print(f"🔄 State transition: {self.pomodoro_timer.get_state_name()}")
            
            # TODO: Trigger notification effects
            # if current_state == STATE_BREAK_SHORT:
            #     print("🎉 Work session completed! Break time!")
            #     self.led_handler.flash_color(0, 255, 0, duration_ms=2000)  # Flash green
            #     self.oled_handler.show_notification("Break Time!", duration_ms=3000)
            # elif current_state == STATE_WORK and self.last_state == STATE_BREAK_SHORT:
            #     print("💪 Break completed! Back to work!")
            #     self.led_handler.flash_color(255, 0, 0, duration_ms=2000)  # Flash red
            #     self.oled_handler.show_notification("Work Time!", duration_ms=3000)
            
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
