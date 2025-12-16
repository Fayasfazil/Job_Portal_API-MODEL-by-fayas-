"""
GUI Entry Point
--------------
This module defines the main application class for the Desktop GUI.
It manages the main window and navigation between different frames
(Login, Register, Dashboard).

Classes:
    JobPortalApp: Main application class.
"""

import customtkinter as ctk
from src.gui.database_service import DatabaseService
from src.gui.auth_ui import LoginFrame, RegisterFrame
from src.gui.dashboard_ui import DashboardFrame
from src.gui.theme import Theme
from src.gui.animator import Animator

class JobPortalApp(ctk.CTk):
    """
    Main Application Class.
    Manages the main window and frame switching.
    """
    def __init__(self):
        super().__init__()

        self.title("Job Portal System")
        self.geometry("1100x700")
        self.minsize(900, 600)
        
        # Set Appearance
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Apply Theme Background (fallback)
        self.configure(fg_color=Theme.BACKGROUND)

        # Initialize Database Service (Standalone)
        self.db_service = DatabaseService()
        self.current_frame = None
        
        # Start Fade In
        Animator.fade_in(self)

        # Start with Login Screen
        self.show_login()

    def switch_frame(self, frame_class, **kwargs):
        """
        Switch the current frame to a new one.

        Args:
            frame_class: The class of the new frame.
            **kwargs: Arguments to pass to the new frame's constructor.
        """
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = frame_class(self, **kwargs)
        self.current_frame.pack(fill="both", expand=True)

    def show_login(self):
        """Switch to Login Frame."""
        self.switch_frame(LoginFrame, 
                          db_service=self.db_service, 
                          on_login_success=self.show_dashboard,
                          on_switch_to_register=self.show_register)

    def show_register(self):
        """Switch to Register Frame."""
        self.switch_frame(RegisterFrame, 
                          db_service=self.db_service, 
                          on_register_success=self.show_login,
                          on_switch_to_login=self.show_login)

    def show_dashboard(self):
        """Switch to Dashboard Frame."""
        self.switch_frame(DashboardFrame, 
                          db_service=self.db_service, 
                          on_logout=self.show_login)

if __name__ == "__main__":
    app = JobPortalApp()
    app.mainloop()
