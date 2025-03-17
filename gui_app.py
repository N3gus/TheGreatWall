"""
Main GUI Application for Chinese Wall Model Demonstration
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
import traceback
import sys
from typing import Optional, Callable, Any

matplotlib.use('TkAgg')  # Set the backend for matplotlib

from chinese_wall_model import ChineseWallModel
from data_manager import DataManager
from report_generator import ReportGenerator
from utils import center_window, create_tooltip, explain_chinese_wall
from login_screen import LoginScreen
from main_dashboard import MainDashboard
from report_screen import ReportScreen
from admin_screen import AdminScreen
from help_screen import HelpScreen

class ChineseWallApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chinese Wall Model Demonstration")
        self.root.minsize(800, 600)
        
        # Set up exception handling
        self.setup_exception_handler()
        
        try:
            # Set up the model and related components
            self.model = ChineseWallModel()
            self.data_manager = DataManager(self.model)
            self.report_generator = ReportGenerator(self.model)
            
            # Initialize sample data
            self.data_manager.initialize_sample_data()
            
            # Set up styles
            self.setup_styles()
            
            # Center the window
            center_window(self.root, 1000, 700)
            
            # Initialize variables
            self.current_user = None
            self.current_frame = None
            
            # Start with the login screen
            self.show_login_screen()
        except Exception as e:
            self.handle_exception("Initialization Error", e)
    
    def setup_exception_handler(self) -> None:
        """Set up global exception handler"""
        def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
            """Handle uncaught exceptions"""
            error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            messagebox.showerror("Unhandled Exception", 
                                f"An unexpected error occurred:\n\n{str(exc_value)}\n\n"
                                f"Please report this issue with the following details:\n\n{error_msg}")
            # Log the error
            print(f"Unhandled Exception:\n{error_msg}", file=sys.stderr)
            # Exit the application
            self.root.quit()
        
        # Set the exception hook
        sys.excepthook = handle_uncaught_exception
    
    def handle_exception(self, title: str, exception: Exception) -> None:
        """Handle exceptions in a user-friendly way"""
        error_msg = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
        messagebox.showerror(title, 
                            f"An error occurred:\n\n{str(exception)}\n\n"
                            f"Technical details:\n{error_msg}")
        # Log the error
        print(f"{title}:\n{error_msg}", file=sys.stderr)
    
    def setup_styles(self) -> None:
        """Set up ttk styles for the application"""
        try:
            style = ttk.Style()
            
            # Configure TButton style
            style.configure('TButton', font=('Arial', 10))
            style.configure('Large.TButton', font=('Arial', 12))
            
            # Configure TLabel style
            style.configure('TLabel', font=('Arial', 10))
            style.configure('Header.TLabel', font=('Arial', 16, 'bold'))
            style.configure('Subheader.TLabel', font=('Arial', 12, 'bold'))
            
            # Configure TFrame style
            style.configure('TFrame', background='#f0f0f0')
            
            # Configure TNotebook style
            style.configure('TNotebook', tabposition='n')
            style.configure('TNotebook.Tab', font=('Arial', 10))
        except Exception as e:
            self.handle_exception("Style Setup Error", e)
    
    def show_login_screen(self) -> None:
        """Display the login screen"""
        try:
            if self.current_frame:
                self.current_frame.destroy()
            
            self.current_frame = LoginScreen(self.root, self.model, self.login_callback)
        except Exception as e:
            self.handle_exception("Login Screen Error", e)
    
    def show_main_dashboard(self) -> None:
        """Display the main dashboard"""
        try:
            if self.current_frame:
                self.current_frame.destroy()
            
            self.current_frame = MainDashboard(
                self.root, 
                self.model, 
                self.data_manager, 
                self.current_user,
                self.logout_callback,
                self.show_report_screen,
                self.show_admin_screen,
                self.show_help_screen
            )
        except Exception as e:
            self.handle_exception("Dashboard Error", e)
    
    def show_report_screen(self) -> None:
        """Display the report screen"""
        try:
            if self.current_frame:
                self.current_frame.destroy()
            
            self.current_frame = ReportScreen(
                self.root, 
                self.model, 
                self.report_generator, 
                self.current_user,
                self.back_to_dashboard
            )
        except Exception as e:
            self.handle_exception("Report Screen Error", e)
    
    def show_admin_screen(self) -> None:
        """Display the admin screen"""
        try:
            if self.current_frame:
                self.current_frame.destroy()
            
            self.current_frame = AdminScreen(
                self.root, 
                self.model, 
                self.data_manager, 
                self.current_user,
                self.back_to_dashboard
            )
        except Exception as e:
            self.handle_exception("Admin Screen Error", e)
    
    def show_help_screen(self) -> None:
        """Display the help screen"""
        try:
            if self.current_frame:
                self.current_frame.destroy()
            
            self.current_frame = HelpScreen(
                self.root,
                self
            )
        except Exception as e:
            self.handle_exception("Help Screen Error", e)
    
    def login_callback(self, user_id: str) -> None:
        """Callback for successful login"""
        try:
            self.current_user = user_id
            self.show_main_dashboard()
        except Exception as e:
            self.handle_exception("Login Error", e)
    
    def logout_callback(self) -> None:
        """Callback for logout"""
        try:
            self.current_user = None
            self.show_login_screen()
        except Exception as e:
            self.handle_exception("Logout Error", e)
    
    def back_to_dashboard(self) -> None:
        """Callback to return to the dashboard"""
        try:
            self.show_main_dashboard()
        except Exception as e:
            self.handle_exception("Navigation Error", e)

def main():
    try:
        root = tk.Tk()
        app = ChineseWallApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Critical Error", 
                            f"A critical error occurred:\n\n{str(e)}\n\n"
                            f"The application will now exit.")
        print(f"Critical Error:\n{traceback.format_exc()}", file=sys.stderr)

if __name__ == "__main__":
    main()
