"""
Dashboard UI Module
------------------
This module defines the main Dashboard with a modern Sidebar + Content layout.
It uses threading for API calls and Card components for data display.

Classes:
    DashboardFrame: Main dashboard UI.
"""

import threading
import customtkinter as ctk
from tkinter import messagebox, simpledialog
from typing import Callable, Any
from src.gui.database_service import DatabaseService
from src.gui.theme import Theme

class DashboardFrame(ctk.CTkFrame):
    """
    Main Dashboard Frame with Sidebar Navigation.
    """
    def __init__(self, master, db_service: DatabaseService, on_logout: Callable):
        super().__init__(master, fg_color=Theme.BACKGROUND)
        self.db_service = db_service
        self.on_logout = on_logout
        
        # State
        self.current_view = "Tasks"

        self._setup_ui()
    
    def _setup_ui(self):
        """Initialize Grid Layout."""
        self.grid_columnconfigure(1, weight=1) # Content area expands
        self.grid_rowconfigure(0, weight=1)

        self._setup_sidebar()
        self._setup_main_content()
        
        # Initial Load
        self.show_tasks()

    def _setup_sidebar(self):
        """Create Left Sidebar."""
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=Theme.SURFACE)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1) # Spacer

        # App Logo / Title
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="NEXUS | PORTAL", font=("Roboto", 24, "bold"), text_color=Theme.ACCENT)
        self.logo_label.grid(row=0, column=0, padx=20, pady=30)

        # Nav Buttons
        self.btn_tasks = self._create_nav_button("OPERATIONS", self.show_tasks, row=1)
        self.btn_orders = self._create_nav_button("LOGISTICS", self.show_orders, row=2)
        
        # User Profile / Logout
        self.user_label = ctk.CTkLabel(self.sidebar_frame, text="OPERATOR", text_color=Theme.TEXT_SECONDARY, font=("Roboto Mono", 12))
        self.user_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        
        self.logout_btn = ctk.CTkButton(self.sidebar_frame, text="TERMINATE SESSION", fg_color="transparent", 
                                        text_color=Theme.ERROR, hover_color="#2b1a1a", border_width=1, border_color=Theme.ERROR,
                                        width=200, height=40, font=("Roboto Mono", 12), command=self.logout)
        self.logout_btn.grid(row=6, column=0, padx=20, pady=20)

    def _create_nav_button(self, text, command, row):
        btn = ctk.CTkButton(self.sidebar_frame, text=text, height=50, corner_radius=0, 
                            fg_color="transparent", text_color=Theme.TEXT_SECONDARY, hover_color=Theme.BACKGROUND,
                            anchor="w", font=("Roboto", 14, "bold"), command=command)
        btn.grid(row=row, column=0, sticky="ew", padx=0, pady=2)
        return btn

    def _setup_main_content(self):
        """Create Main Content Area."""
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=40, pady=40)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Header Area
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=60)
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        self.page_title = ctk.CTkLabel(self.header_frame, text="DASHBOARD", font=("Roboto", 36, "bold"), text_color=Theme.ACCENT)
        self.page_title.pack(side="left")

        self.action_btn = ctk.CTkButton(self.header_frame, text="INITIATE NEW", font=("Roboto Mono", 14, "bold"), 
                                        fg_color=Theme.ACCENT, text_color=Theme.BACKGROUND, hover_color="#ffffff",
                                        width=150, height=40, corner_radius=0, command=self.handle_action)
        self.action_btn.pack(side="right")

        # Scrollable Content List
        self.content_scroll = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        self.content_scroll.grid(row=1, column=0, sticky="nsew")

    # ---------- Navigation Handlers ----------

    def _highlight_nav(self, active_btn):
        # Reset colors
        self.btn_tasks.configure(fg_color="transparent", text_color=Theme.TEXT_SECONDARY)
        self.btn_orders.configure(fg_color="transparent", text_color=Theme.TEXT_SECONDARY)
        # Highlight
        active_btn.configure(fg_color=Theme.BACKGROUND, text_color=Theme.ACCENT)

    def show_tasks(self):
        self.current_view = "Tasks"
        self.page_title.configure(text="ACTIVE OPERATIONS")
        self.action_btn.configure(text="NEW OPERATION", command=self.add_task_dialog)
        self._highlight_nav(self.btn_tasks)
        self.load_tasks()

    def show_orders(self):
        self.current_view = "Orders"
        self.page_title.configure(text="LOGISTICS MANIFEST")
        self.action_btn.configure(text="NEW ORDER", command=self.add_order_dialog)
        self._highlight_nav(self.btn_orders)
        self.load_orders()

    def logout(self):
        self.db_service.logout()
        self.on_logout()

    # ---------- Data Logic (Tasks) ----------

    def load_tasks(self):
        # Clear UI
        for widget in self.content_scroll.winfo_children():
            widget.destroy()
        
        loading = ctk.CTkLabel(self.content_scroll, text="RETRIEVING DATA...", font=("Roboto Mono", 16), text_color=Theme.TEXT_SECONDARY)
        loading.pack(pady=50)

        threading.Thread(target=self._fetch_tasks_thread, daemon=True).start()

    def _fetch_tasks_thread(self):
        try:
            data = self.db_service.get_tasks()
            self.after(0, self._update_tasks_ui, data)
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", str(e)))

    def _update_tasks_ui(self, data: Any):
        # Clear loading
        for widget in self.content_scroll.winfo_children():
            widget.destroy()

        tasks = data.get('tasks', [])
        if not tasks:
            ctk.CTkLabel(self.content_scroll, text="NO ACTIVE OPERATIONS FOUND", font=("Roboto Mono", 16), text_color=Theme.TEXT_SECONDARY).pack(pady=50)
            return

        for task in tasks:
            self._create_task_card(task)

    def _create_task_card(self, task):
        # Card Frame
        card = ctk.CTkFrame(self.content_scroll, fg_color=Theme.SURFACE, corner_radius=0, border_width=1, border_color="#333333")
        card.pack(fill="x", pady=5, padx=0)

        # Status Indicator (Monochrome: Filled vs Empty or similar)
        # We'll use text color for subtle indication
        status_color = Theme.ACCENT if task['status'] == 'completed' else Theme.TEXT_SECONDARY
        
        # Info
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, pady=15, padx=20)

        ctk.CTkLabel(info_frame, text=task['title'].upper(), font=("Roboto", 16, "bold"), text_color=Theme.TEXT).pack(anchor="w")
        if task.get('description'):
            ctk.CTkLabel(info_frame, text=task.get('description', ''), text_color=Theme.TEXT_SECONDARY, font=("Roboto", 12)).pack(anchor="w")
        
        # Meta
        meta_frame = ctk.CTkFrame(card, fg_color="transparent")
        meta_frame.pack(side="right", padx=20)

        ctk.CTkLabel(meta_frame, text=f"STATUS: {task['status'].upper()}", font=("Roboto Mono", 12), text_color=status_color).pack(anchor="e")
        
        del_btn = ctk.CTkButton(meta_frame, text="DELETE", width=60, height=25, fg_color="transparent", 
                                text_color=Theme.ERROR, hover_color="#2b1a1a", font=("Roboto Mono", 10),
                                command=lambda t=task['id']: self.delete_task(t))
        del_btn.pack(pady=(5, 0))

    def add_task_dialog(self):
        dialog = ctk.CTkInputDialog(text="ENTER OPERATION TITLE:", title="NEW TASK")
        title = dialog.get_input()
        if title:
            threading.Thread(target=self._create_task_thread, args=(title,), daemon=True).start()

    def _create_task_thread(self, title: str):
        try:
            success = self.db_service.create_task(title, "Created via Console")
            self.after(0, lambda: self.load_tasks() if success else messagebox.showerror("Error", "Failed"))
        except Exception as e:
            print(e)
            
    def delete_task(self, task_id):
        threading.Thread(target=lambda: self._delete_task_thread(task_id), daemon=True).start()

    def _delete_task_thread(self, task_id):
        success = self.db_service.delete_task(task_id)
        self.after(0, lambda: self.load_tasks() if success else messagebox.showerror("Delete Failed", "Could not delete task"))

    # ---------- Data Logic (Orders) ----------

    def handle_action(self):
        if self.current_view == "Tasks":
            self.add_task_dialog()
        else:
            self.add_order_dialog()

    def load_orders(self):
        for widget in self.content_scroll.winfo_children():
            widget.destroy()
            
        loading = ctk.CTkLabel(self.content_scroll, text="RETRIEVING DATA...", font=("Roboto Mono", 16), text_color=Theme.TEXT_SECONDARY)
        loading.pack(pady=50)
        
        threading.Thread(target=self._fetch_orders_thread, daemon=True).start()

    def _fetch_orders_thread(self):
        try:
            data = self.db_service.get_orders()
            self.after(0, self._update_orders_ui, data)
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", str(e)))

    def _update_orders_ui(self, data: Any):
        for widget in self.content_scroll.winfo_children():
            widget.destroy()

        orders = data.get('orders', [])
        if not orders:
            ctk.CTkLabel(self.content_scroll, text="NO LOGISTICS DATA FOUND", font=("Roboto Mono", 16), text_color=Theme.TEXT_SECONDARY).pack(pady=50)
            return

        for order in orders:
            self._create_order_card(order)

    def _create_order_card(self, order):
        card = ctk.CTkFrame(self.content_scroll, fg_color=Theme.SURFACE, corner_radius=0, border_width=1, border_color="#333333")
        card.pack(fill="x", pady=5, padx=0)

        # Info
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, pady=15, padx=20)

        ctk.CTkLabel(info_frame, text=order['product_name'].upper(), font=("Roboto", 16, "bold"), text_color=Theme.TEXT).pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"QTY: {order['quantity']} | UNIT PRICE: ${order['price']}", text_color=Theme.TEXT_SECONDARY, font=("Roboto Mono", 12)).pack(anchor="w")

        # Total Price
        total = order['quantity'] * order['price']
        ctk.CTkLabel(card, text=f"${total:.2f}", font=("Roboto Mono", 18, "bold"), text_color=Theme.ACCENT).pack(side="right", padx=20)

    def add_order_dialog(self):
        dialog = ctk.CTkInputDialog(text="ENTER ITEM IDENTIFIER:", title="NEW ORDER")
        name = dialog.get_input()
        if name:
            threading.Thread(target=self._create_order_thread, args=(name,), daemon=True).start()

    def _create_order_thread(self, name: str):
        success = self.db_service.create_order(name, 99.99, 1)
        self.after(0, lambda: self.load_orders() if success else messagebox.showerror("Error", "Failed"))
