"""
Animator Module
--------------
Provides animation utilities to add life to the GUI.
"""

import customtkinter as ctk
import time

class Animator:
    @staticmethod
    def fade_in(window: ctk.CTk, duration: float = 0.5, steps: int = 20):
        """
        Fade in the main window by gradually increasing alpha.
        """
        window.attributes("-alpha", 0.0)
        step_time = duration / steps
        alpha_step = 1.0 / steps
        
        def _step(current_alpha):
            if current_alpha >= 1.0:
                window.attributes("-alpha", 1.0)
                return
            
            window.attributes("-alpha", current_alpha)
            window.after(int(step_time * 1000), lambda: _step(current_alpha + alpha_step))
            
        _step(0.0)

    @staticmethod
    def slide_up(widget: ctk.CTkFrame, start_y: float, end_y: float, duration: float = 0.4, steps: int = 20):
        """
        Animate a widget sliding up (using place or grid padding simulation).
        Note: For grid, we simulate slide by adjusting pady.
        """
        # This implementation assumes the widget is using .grid() and we are animating pady
        # decreasing from a large value to a small value.
        
        step_time = duration / steps
        dist = start_y - end_y
        step_dist = dist / steps
        
        def _step(current_y):
            if current_y <= end_y:
                widget.grid_configure(pady=(end_y, 0)) # Clean finish
                return
            
            # Update padding top
            widget.grid_configure(pady=(int(current_y), 0))
            widget.after(int(step_time * 1000), lambda: _step(current_y - step_dist))
            
        _step(start_y)
