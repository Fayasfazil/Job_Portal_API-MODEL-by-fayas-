import customtkinter as ctk
from tkinter import messagebox
from typing import Callable
from src.gui.database_service import DatabaseService
from src.gui.theme import Theme
from src.gui.animator import Animator

class LoginFrame(ctk.CTkFrame):
    """
    Frame for User Login with 'Stealth Mode' Design.
    """
    def __init__(self, master, db_service: DatabaseService, on_login_success: Callable, on_switch_to_register: Callable):
        super().__init__(master, fg_color="transparent")
        self.db_service = db_service
        self.on_login_success = on_login_success
        self.on_switch_to_register = on_switch_to_register

        self._setup_ui()
        # Animate inner card
        self.after(100, lambda: Animator.slide_up(self.card, 300, 20))

    def _setup_ui(self):
        """Initialize UI components."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Login Card (Starts lower for animation)
        self.card = ctk.CTkFrame(self, width=380, corner_radius=0, fg_color=Theme.SURFACE, border_width=1, border_color="#333333")
        self.card.grid(row=0, column=0, padx=20, pady=300) # Start low using bad padding, will be animated to 20
        self.card.grid_columnconfigure(0, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(self.card, text="ACCESS CONTROL", font=("Roboto", 32, "bold"), text_color=Theme.ACCENT)
        self.title_label.grid(row=0, column=0, padx=20, pady=(50, 5))

        self.subtitle_label = ctk.CTkLabel(self.card, text="Identify yourself", font=("Roboto Light", 16), text_color=Theme.TEXT_SECONDARY)
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 40))

        # Inputs
        self.email_entry = ctk.CTkEntry(self.card, placeholder_text="ID / EMAIL", 
                                        width=300, height=50, corner_radius=0, 
                                        fg_color=Theme.INPUT_BG, text_color=Theme.INPUT_FG,
                                        border_width=0, font=("Roboto Mono", 14))
        self.email_entry.grid(row=2, column=0, padx=20, pady=10)

        self.password_entry = ctk.CTkEntry(self.card, placeholder_text="PASSWORD", show="•", 
                                           width=300, height=50, corner_radius=0,
                                           fg_color=Theme.INPUT_BG, text_color=Theme.INPUT_FG,
                                           border_width=0, font=("Roboto Mono", 14))
        self.password_entry.grid(row=3, column=0, padx=20, pady=10)

        # Buttons
        self.login_button = ctk.CTkButton(self.card, text="AUTHENTICATE", width=300, height=50, corner_radius=0, 
                                          font=("Roboto", 14, "bold"), fg_color=Theme.ACCENT, text_color=Theme.BACKGROUND,
                                          hover_color="#cccccc",
                                          command=self.login)
        self.login_button.grid(row=4, column=0, padx=20, pady=(30, 10))

        self.register_link = ctk.CTkButton(self.card, text="NO CREDENTIALS? APPLY", 
                                           fg_color="transparent", text_color=Theme.TEXT_SECONDARY, hover_color=Theme.SURFACE,
                                           font=("Roboto", 12),
                                           command=self.on_switch_to_register)
        self.register_link.grid(row=5, column=0, padx=20, pady=(0, 50))

    def login(self):
        """Handle login logic."""
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please fill all fields")
            return

        self.login_button.configure(state="disabled", text="VERIFYING...")
        self.update()

        success, msg = self.db_service.login(email, password)
        
        self.login_button.configure(state="normal", text="AUTHENTICATE")
        
        if success:
            self.on_login_success()
        else:
            messagebox.showerror("Access Denied", msg)

class RegisterFrame(ctk.CTkFrame):
    """
    Frame for User Registration with 'Stealth Mode' Design.
    """
    def __init__(self, master, db_service: DatabaseService, on_register_success: Callable, on_switch_to_login: Callable):
        super().__init__(master, fg_color="transparent")
        self.db_service = db_service
        self.on_register_success = on_register_success
        self.on_switch_to_login = on_switch_to_login

        self._setup_ui()
        self.after(100, lambda: Animator.slide_up(self.card, 300, 20))

    def _setup_ui(self):
        """Initialize UI components."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Card
        self.card = ctk.CTkFrame(self, width=380, corner_radius=0, fg_color=Theme.SURFACE, border_width=1, border_color="#333333")
        self.card.grid(row=0, column=0, padx=20, pady=300)
        self.card.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.card, text="NEW PROFILE", font=("Roboto", 32, "bold"), text_color=Theme.ACCENT)
        self.title_label.grid(row=0, column=0, padx=20, pady=(50, 5))
        
        self.subtitle_label = ctk.CTkLabel(self.card, text="Enter system details", font=("Roboto Light", 16), text_color=Theme.TEXT_SECONDARY)
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 40))

        # Inputs
        self.username_entry = ctk.CTkEntry(self.card, placeholder_text="CODENAME", width=300, height=50, corner_radius=0, 
                                           fg_color=Theme.INPUT_BG, text_color=Theme.INPUT_FG, border_width=0, font=("Roboto Mono", 14))
        self.username_entry.grid(row=2, column=0, padx=20, pady=10)

        self.email_entry = ctk.CTkEntry(self.card, placeholder_text="EMAIL LINK", width=300, height=50, corner_radius=0, 
                                        fg_color=Theme.INPUT_BG, text_color=Theme.INPUT_FG, border_width=0, font=("Roboto Mono", 14))
        self.email_entry.grid(row=3, column=0, padx=20, pady=10)

        self.password_entry = ctk.CTkEntry(self.card, placeholder_text="SECURE KEY", show="•", width=300, height=50, corner_radius=0, 
                                           fg_color=Theme.INPUT_BG, text_color=Theme.INPUT_FG, border_width=0, font=("Roboto Mono", 14))
        self.password_entry.grid(row=4, column=0, padx=20, pady=10)

        # Buttons
        self.register_button = ctk.CTkButton(self.card, text="INITIALIZE", width=300, height=50, corner_radius=0,
                                             font=("Roboto", 14, "bold"), fg_color=Theme.ACCENT, text_color=Theme.BACKGROUND,
                                             hover_color="#cccccc",
                                             command=self.register)
        self.register_button.grid(row=5, column=0, padx=20, pady=(30, 10))

        self.login_link = ctk.CTkButton(self.card, text="ALREADY IN SYSTEM? LOGIN", 
                                        fg_color="transparent", text_color=Theme.TEXT_SECONDARY, hover_color=Theme.SURFACE,
                                        font=("Roboto", 12),
                                        command=self.on_switch_to_login)
        self.login_link.grid(row=6, column=0, padx=20, pady=(0, 50))

    def register(self):
        """Handle registration logic."""
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not username or not email or not password:
            messagebox.showerror("Error", "Please fill all fields")
            return

        self.register_button.configure(state="disabled", text="PROCESSING...")
        self.update()

        success, msg = self.db_service.register(username, email, password)
        
        self.register_button.configure(state="normal", text="INITIALIZE")

        if success:
            messagebox.showinfo("Success", "Profile Created. Proceed to Authentication.")
            self.on_register_success()
        else:
            messagebox.showerror("Error", msg)
