"""
StudyStreak Pomodoro Timer Logic Module
=======================================

This module provides the core Pomodoro timer logic for the ESP32-based StudyStreak project.
It manages timing and state transitions without any hardware interaction.

Author: StudyStreak Project
Environment: MicroPython for ESP32
"""

import utime

# State constants
STATE_IDLE = 0
STATE_WORK = 1
STATE_BREAK_SHORT = 2

# Default durations in minutes (configurable)
DEFAULT_WORK_DURATION_MIN = 45
DEFAULT_BREAK_SHORT_DURATION_MIN = 5

class PomodoroTimer:
    """
    Core Pomodoro timer logic class.
    
    Manages timing, state transitions, and provides interfaces for querying
    current state and remaining time without any hardware dependencies.
    """
    
    def __init__(self, work_mins=DEFAULT_WORK_DURATION_MIN, break_mins=DEFAULT_BREAK_SHORT_DURATION_MIN):
        """
        Initialize the Pomodoro timer.
        
        Args:
            work_mins (int): Work session duration in minutes (default: 45)
            break_mins (int): Short break duration in minutes (default: 5)
        """
        # Convert minutes to seconds for internal use
        self.work_duration_seconds = work_mins * 60
        self.break_duration_seconds = break_mins * 60
        
        # State management
        self.current_state = STATE_IDLE
        self.is_paused = False
        
        # Time tracking
        self.start_time_ms = 0
        self.remaining_time_seconds = 0
        
    def start_work(self):
        """
        Start a work session.
        
        Transitions to STATE_WORK and initializes timing.
        """
        self.current_state = STATE_WORK
        self.remaining_time_seconds = self.work_duration_seconds
        self.start_time_ms = utime.ticks_ms()
        self.is_paused = False
        
    def start_break(self):
        """
        Start a short break session.
        
        Transitions to STATE_BREAK_SHORT and initializes timing.
        """
        self.current_state = STATE_BREAK_SHORT
        self.remaining_time_seconds = self.break_duration_seconds
        self.start_time_ms = utime.ticks_ms()
        self.is_paused = False
    def pause(self):
        """
        Pause the current session.
        
        Can only pause when not in IDLE state and not already paused.
        Preserves current remaining_time_seconds.
        """
        if self.current_state != STATE_IDLE and not self.is_paused:
            self.is_paused = True
            
    def resume(self):
        """
        Resume a paused session.
        
        Updates start_time_ms to current time to continue from where paused.
        """
        if self.is_paused:
            self.is_paused = False
            self.start_time_ms = utime.ticks_ms()
            
    def reset(self):
        """
        Reset the timer to IDLE state.
        
        Clears all timing and state information.
        """
        self.current_state = STATE_IDLE
        self.is_paused = False
        self.start_time_ms = 0
        self.remaining_time_seconds = 0
        
    def update(self):
        """
        Update the timer state and remaining time.
        
        This method should be called frequently from the main application loop.
        Handles automatic state transitions when sessions complete.
        """
        # Only update if not IDLE and not paused
        if self.current_state == STATE_IDLE or self.is_paused:
            return
            
        # Calculate elapsed time since start or resume
        current_time_ms = utime.ticks_ms()
        elapsed_ms = utime.ticks_diff(current_time_ms, self.start_time_ms)
        elapsed_seconds = elapsed_ms // 1000
        
        # Only process if at least 1 second has elapsed
        if elapsed_seconds == 0:
            return
        
        # Update remaining time
        self.remaining_time_seconds -= elapsed_seconds
        
        # Update start time for next calculation
        self.start_time_ms = current_time_ms
        
        # Check for session completion and handle state transitions
        if self.remaining_time_seconds <= 0:
            if self.current_state == STATE_WORK:
                # Work session completed, start break
                self.start_break()
            elif self.current_state == STATE_BREAK_SHORT:
                # Break completed, start new work session
                self.start_work()
                
    def get_state(self):
        """
        Get the current timer state.
        
        Returns:
            int: Current state (STATE_IDLE, STATE_WORK, or STATE_BREAK_SHORT)        """
        return self.current_state
        
    def get_remaining_time_str(self):
        """
        Get remaining time as a formatted string.
        
        Returns:
            str: Time in "MM:SS" format, minimum "00:00"
        """
        # Ensure we don't show negative time and convert to integer
        remaining = max(0, int(self.remaining_time_seconds))
        
        minutes = remaining // 60
        seconds = remaining % 60
        
        return f"{minutes:02d}:{seconds:02d}"
    def get_remaining_seconds(self):
        """
        Get remaining time in seconds.
        
        Returns:
            int: Remaining seconds (minimum 0)
        """
        return max(0, int(self.remaining_time_seconds))
        
    def is_timer_paused(self):
        """
        Check if the timer is currently paused.
        
        Returns:
            bool: True if paused, False otherwise
        """
        return self.is_paused
          def get_state_name(self):
        """
        Get human-readable state name.
        
        Returns:
            str: State name ("IDLE", "WORK", "BREAK_SHORT")
        """
        state_names = {
            STATE_IDLE: "IDLE",
            STATE_WORK: "WORK",
            STATE_BREAK_SHORT: "BREAK_SHORT"
        }
        return state_names.get(self.current_state, "UNKNOWN")
        
    def get_session_progress_percent(self):
        """
        Get current session progress as a percentage.
        
        Returns:
            float: Progress percentage (0.0 to 100.0), or 0.0 if IDLE
        """
        if self.current_state == STATE_IDLE:
            return 0.0
        elif self.current_state == STATE_WORK:
            total_duration = self.work_duration_seconds
        elif self.current_state == STATE_BREAK_SHORT:
            total_duration = self.break_duration_seconds
        else:
            return 0.0
            
        elapsed = total_duration - max(0, self.remaining_time_seconds)
        return min(100.0, (elapsed / total_duration) * 100.0)

# Example usage (commented out - for reference only)
"""
# Create a Pomodoro timer with default durations (45min work, 5min break)
timer = PomodoroTimer()

# Or create with custom durations
# timer = PomodoroTimer(work_mins=25, break_mins=5)

# Start a work session
timer.start_work()

# Main loop example
while True:
    # Update timer state (call this frequently in your main loop)
    timer.update()
    
    # Get current information
    state = timer.get_state()
    remaining = timer.get_remaining_time_str()
    state_name = timer.get_state_name()
    
    print(f"State: {state_name}, Time: {remaining}")
    
    # Example of pausing/resuming
    # timer.pause()
    # timer.resume()
    
    # Example of resetting
    # timer.reset()
    
    # Sleep briefly to avoid overwhelming output
    utime.sleep_ms(1000)
"""