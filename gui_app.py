"""
Main GUI Application for Chinese Wall Model Demonstration
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
import traceback
import sys
import time
from typing import Optional, Callable, Any
from PIL import Image, ImageTk

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

class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.splash = tk.Toplevel(root)
        self.splash.title("Loading...")
        self.splash.attributes("-topmost", True)
        
        # Remove window decorations
        self.splash.overrideredirect(True)
        
        # Set size and position
        width, height = 500, 300
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.splash.geometry(f"{width}x{height}+{x}+{y}")
        
        # Create a frame with a border
        main_frame = tk.Frame(self.splash, bg="#f0f0f0", bd=2, relief=tk.RIDGE)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Add a title
        title_label = tk.Label(main_frame, text="Chinese Wall Model", 
                              font=("Arial", 24, "bold"), bg="#f0f0f0")
        title_label.pack(pady=(40, 10))
        
        subtitle_label = tk.Label(main_frame, text="Security Demonstration", 
                                font=("Arial", 16), bg="#f0f0f0")
        subtitle_label.pack(pady=(0, 30))
        
        # Add a progress bar
        self.progress = ttk.Progressbar(main_frame, orient="horizontal", 
                                       length=400, mode="determinate")
        self.progress.pack(pady=20)
        
        # Add a status label
        self.status_var = tk.StringVar(value="Initializing...")
        status_label = tk.Label(main_frame, textvariable=self.status_var, 
                              font=("Arial", 10), bg="#f0f0f0")
        status_label.pack(pady=10)
        
        # Add copyright
        copyright_label = tk.Label(main_frame, text=" 2025 Chinese Wall Demo", 
                                 font=("Arial", 8), bg="#f0f0f0")
        copyright_label.pack(side=tk.BOTTOM, pady=10)
        
        # Update the splash screen
        self.splash.update()
    
    def update_progress(self, value, status_text):
        """Update the progress bar and status text"""
        self.progress["value"] = value
        self.status_var.set(status_text)
        self.splash.update()
        time.sleep(0.1)  # Small delay to show progress
    
    def destroy(self):
        """Destroy the splash screen"""
        self.splash.destroy()

class ChineseWallApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chinese Wall Model Demonstration")
        self.root.minsize(900, 700)
        
        # Set up exception handling
        self.setup_exception_handler()
        
        # Create splash screen
        splash = SplashScreen(self.root)
        
        try:
            # Set up the model and related components
            splash.update_progress(20, "Initializing model...")
            self.model = ChineseWallModel()
            
            splash.update_progress(40, "Setting up data manager...")
            self.data_manager = DataManager(self.model)
            
            splash.update_progress(60, "Setting up report generator...")
            self.report_generator = ReportGenerator(self.model)
            
            # Initialize sample data
            splash.update_progress(80, "Loading sample data...")
            self.data_manager.initialize_sample_data()
            
            # Set up styles
            splash.update_progress(90, "Setting up UI...")
            self.setup_styles()
            
            # Center the window
            center_window(self.root, 1100, 750)
            
            # Initialize variables
            self.current_user = None
            self.current_frame = None
            
            # Create status bar
            self.create_status_bar()
            
            # Complete loading
            splash.update_progress(100, "Ready!")
            time.sleep(0.5)
            splash.destroy()
            
            # Start with the login screen
            self.show_login_screen()
            
        except Exception as e:
            splash.destroy()
            self.handle_exception("Initialization Error", e)
    
    def setup_exception_handler(self) -> None:
        """Set up global exception handler"""
        def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
            """Handle uncaught exceptions"""
            error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            
            # Create a custom error dialog
            error_window = tk.Toplevel(self.root)
            error_window.title("Unhandled Exception")
            error_window.grab_set()  # Make the window modal
            
            # Set size and center the window
            width, height = 600, 400
            screen_width = error_window.winfo_screenwidth()
            screen_height = error_window.winfo_screenheight()
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
            error_window.geometry(f"{width}x{height}+{x}+{y}")
            
            # Create the content
            main_frame = ttk.Frame(error_window, padding=20)
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Error icon and title in a frame
            header_frame = ttk.Frame(main_frame)
            header_frame.pack(fill=tk.X, pady=(0, 20))
            
            # Error icon (using text as a placeholder)
            icon_label = ttk.Label(header_frame, text="", font=("Arial", 24))
            icon_label.pack(side=tk.LEFT, padx=(0, 10))
            
            # Error title
            title_label = ttk.Label(header_frame, text="An unexpected error occurred", 
                                   font=("Arial", 14, "bold"))
            title_label.pack(side=tk.LEFT)
            
            # Error message
            message_label = ttk.Label(main_frame, text=str(exc_value), 
                                     wraplength=550, justify=tk.LEFT)
            message_label.pack(fill=tk.X, pady=10)
            
            # Technical details in a scrolled text
            details_frame = ttk.LabelFrame(main_frame, text="Technical Details")
            details_frame.pack(fill=tk.BOTH, expand=True, pady=10)
            
            details_text = tk.Text(details_frame, wrap=tk.WORD, height=10, 
                                  font=("Courier", 9))
            details_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Add a scrollbar
            scrollbar = ttk.Scrollbar(details_text, command=details_text.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            details_text.config(yscrollcommand=scrollbar.set)
            
            # Insert the error details
            details_text.insert(tk.END, error_msg)
            details_text.config(state=tk.DISABLED)
            
            # Buttons frame
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill=tk.X, pady=20)
            
            # Copy to clipboard button
            def copy_to_clipboard():
                self.root.clipboard_clear()
                self.root.clipboard_append(error_msg)
                self.root.update()
            
            copy_button = ttk.Button(button_frame, text="Copy to Clipboard", 
                                    command=copy_to_clipboard)
            copy_button.pack(side=tk.LEFT)
            
            # Close button
            close_button = ttk.Button(button_frame, text="Close", 
                                     command=error_window.destroy)
            close_button.pack(side=tk.RIGHT)
            
            # Log the error
            print(f"Unhandled Exception:\n{error_msg}", file=sys.stderr)
        
        # Set the exception hook
        sys.excepthook = handle_uncaught_exception
    
    def handle_exception(self, title: str, exception: Exception) -> None:
        """Handle exceptions in a user-friendly way"""
        error_msg = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
        
        # Create a custom error dialog
        error_window = tk.Toplevel(self.root)
        error_window.title(title)
        error_window.grab_set()  # Make the window modal
        
        # Set size and center the window
        width, height = 600, 400
        screen_width = error_window.winfo_screenwidth()
        screen_height = error_window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        error_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Create the content
        main_frame = ttk.Frame(error_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Error icon and title in a frame
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Error icon (using text as a placeholder)
        icon_label = ttk.Label(header_frame, text="", font=("Arial", 24))
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Error title
        title_label = ttk.Label(header_frame, text=title, 
                               font=("Arial", 14, "bold"))
        title_label.pack(side=tk.LEFT)
        
        # Error message
        message_label = ttk.Label(main_frame, text=str(exception), 
                                 wraplength=550, justify=tk.LEFT)
        message_label.pack(fill=tk.X, pady=10)
        
        # Technical details in a scrolled text
        details_frame = ttk.LabelFrame(main_frame, text="Technical Details")
        details_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        details_text = tk.Text(details_frame, wrap=tk.WORD, height=10, 
                              font=("Courier", 9))
        details_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(details_text, command=details_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        details_text.config(yscrollcommand=scrollbar.set)
        
        # Insert the error details
        details_text.insert(tk.END, error_msg)
        details_text.config(state=tk.DISABLED)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        # Copy to clipboard button
        def copy_to_clipboard():
            self.root.clipboard_clear()
            self.root.clipboard_append(error_msg)
            self.root.update()
        
        copy_button = ttk.Button(button_frame, text="Copy to Clipboard", 
                                command=copy_to_clipboard)
        copy_button.pack(side=tk.LEFT)
        
        # Close button
        close_button = ttk.Button(button_frame, text="Close", 
                                 command=error_window.destroy)
        close_button.pack(side=tk.RIGHT)
        
        # Log the error
        print(f"{title}:\n{error_msg}", file=sys.stderr)
    
    def setup_styles(self) -> None:
        """Set up ttk styles for the application"""
        try:
            # Create a modern theme
            style = ttk.Style()
            
            # Try to use a more modern theme if available
            available_themes = style.theme_names()
            if 'clam' in available_themes:
                style.theme_use('clam')
            
            # Define colors
            primary_color = "#1976d2"  # Blue
            secondary_color = "#f0f0f0"  # Light gray
            accent_color = "#ff9800"  # Orange
            text_color = "#212121"  # Dark gray
            light_text_color = "#757575"  # Medium gray
            
            # Configure TButton style
            style.configure('TButton', 
                           font=('Arial', 10),
                           background=primary_color,
                           foreground=text_color,
                           padding=5)
            
            style.map('TButton',
                     background=[('active', accent_color), ('pressed', primary_color)],
                     relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
            
            # Large button style
            style.configure('Large.TButton', 
                           font=('Arial', 12, 'bold'),
                           padding=8)
            
            # Accent button style
            style.configure('Accent.TButton',
                           background=accent_color)
            
            # Configure TLabel style
            style.configure('TLabel', 
                           font=('Arial', 10),
                           foreground=text_color)
            
            # Header styles
            style.configure('Header.TLabel', 
                           font=('Arial', 18, 'bold'),
                           foreground=primary_color)
            
            style.configure('Subheader.TLabel', 
                           font=('Arial', 14, 'bold'),
                           foreground=text_color)
            
            # Configure TFrame style
            style.configure('TFrame', background=secondary_color)
            
            # Configure TLabelframe style
            style.configure('TLabelframe', 
                           background=secondary_color,
                           foreground=text_color)
            
            style.configure('TLabelframe.Label', 
                           font=('Arial', 11, 'bold'),
                           foreground=primary_color)
            
            # Configure TNotebook style
            style.configure('TNotebook', 
                           background=secondary_color,
                           tabposition='n')
            
            style.configure('TNotebook.Tab', 
                           font=('Arial', 10),
                           padding=[10, 4],
                           background=secondary_color)
            
            style.map('TNotebook.Tab',
                     background=[('selected', primary_color), ('active', accent_color)],
                     foreground=[('selected', 'white'), ('active', 'black')])
            
            # Configure TEntry style
            style.configure('TEntry', 
                           font=('Arial', 10),
                           fieldbackground='white')
            
            # Configure TCombobox style
            style.configure('TCombobox', 
                           font=('Arial', 10),
                           fieldbackground='white')
            
            # Configure Treeview
            style.configure('Treeview', 
                           font=('Arial', 10),
                           background='white',
                           fieldbackground='white')
            
            style.configure('Treeview.Heading', 
                           font=('Arial', 10, 'bold'),
                           background=secondary_color)
            
            # Status bar style
            style.configure('StatusBar.TLabel',
                           font=('Arial', 9),
                           foreground=light_text_color,
                           background='#e0e0e0',
                           padding=2)
            
        except Exception as e:
            self.handle_exception("Style Setup Error", e)
    
    def create_status_bar(self):
        """Create a status bar at the bottom of the window"""
        self.status_bar = ttk.Frame(self.root, style='StatusBar.TFrame')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Status message
        self.status_message = tk.StringVar(value="Ready")
        status_label = ttk.Label(self.status_bar, textvariable=self.status_message,
                                style='StatusBar.TLabel')
        status_label.pack(side=tk.LEFT, padx=5)
        
        # Add a separator
        separator = ttk.Separator(self.status_bar, orient=tk.VERTICAL)
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)
        
        # User info (will be updated when logged in)
        self.user_info = tk.StringVar(value="Not logged in")
        user_label = ttk.Label(self.status_bar, textvariable=self.user_info,
                              style='StatusBar.TLabel')
        user_label.pack(side=tk.LEFT, padx=5)
        
        # Right side of status bar
        # Current time
        self.time_var = tk.StringVar()
        time_label = ttk.Label(self.status_bar, textvariable=self.time_var,
                              style='StatusBar.TLabel')
        time_label.pack(side=tk.RIGHT, padx=5)
        
        # Update time periodically
        self.update_time()
    
    def update_time(self):
        """Update the time display in the status bar"""
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%Y-%m-%d")
        self.time_var.set(f"{current_date} {current_time}")
        self.root.after(1000, self.update_time)
    
    def update_status(self, message):
        """Update the status bar message"""
        self.status_message.set(message)
    
    def show_login_screen(self) -> None:
        """Display the login screen"""
        try:
            if self.current_frame:
                self.current_frame.destroy()
            
            self.update_status("Please log in")
            self.user_info.set("Not logged in")
            
            self.current_frame = LoginScreen(self.root, self.model, self.login_callback)
        except Exception as e:
            self.handle_exception("Login Screen Error", e)
    
    def show_main_dashboard(self) -> None:
        """Display the main dashboard"""
        try:
            if self.current_frame:
                self.current_frame.destroy()
            
            self.update_status("Main Dashboard")
            user_info = self.model.users.get(self.current_user, {})
            self.user_info.set(f"Logged in as: {user_info.get('name', self.current_user)}")
            
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
            
            self.update_status("Viewing Reports")
            
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
            
            self.update_status("Administrator Panel")
            
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
            
            self.update_status("Help & Information")
            
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
            user_info = self.model.users.get(user_id, {})
            self.update_status(f"Logged in as {user_info.get('name', user_id)}")
            self.show_main_dashboard()
        except Exception as e:
            self.handle_exception("Login Error", e)
    
    def logout_callback(self) -> None:
        """Callback for logout"""
        try:
            self.current_user = None
            self.update_status("Logged out")
            self.show_login_screen()
        except Exception as e:
            self.handle_exception("Logout Error", e)
    
    def back_to_dashboard(self) -> None:
        """Callback to return to the dashboard"""
        try:
            self.update_status("Returning to dashboard")
            self.show_main_dashboard()
        except Exception as e:
            self.handle_exception("Navigation Error", e)

def main():
    """Main entry point for the application"""
    root = tk.Tk()
    app = ChineseWallApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
