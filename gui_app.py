"""
Main GUI Application for Chinese Wall Model Demonstration
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
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
    
    def setup_styles(self):
        """Set up ttk styles for the application"""
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
    
    def show_login_screen(self):
        """Display the login screen"""
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = LoginScreen(self.root, self.model, self.login_callback)
    
    def show_main_dashboard(self):
        """Display the main dashboard"""
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
    
    def show_report_screen(self):
        """Display the report screen"""
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = ReportScreen(
            self.root, 
            self.model, 
            self.report_generator, 
            self.current_user,
            self.back_to_dashboard
        )
    
    def show_admin_screen(self):
        """Display the admin screen"""
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = AdminScreen(
            self.root, 
            self.model, 
            self.data_manager, 
            self.current_user,
            self.back_to_dashboard
        )
    
    def show_help_screen(self):
        """Display the help screen"""
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = HelpScreen(
            self.root,
            self
        )
    
    def login_callback(self, user_id):
        """Callback for successful login"""
        self.current_user = user_id
        self.show_main_dashboard()
    
    def logout_callback(self):
        """Callback for logout"""
        self.current_user = None
        self.show_login_screen()
    
    def back_to_dashboard(self):
        """Callback to return to the dashboard"""
        self.show_main_dashboard()

def main():
    root = tk.Tk()
    app = ChineseWallApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
