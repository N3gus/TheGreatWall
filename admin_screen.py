"""
Admin Screen for Chinese Wall Model Demonstration
Main container with tabs for different admin functions
"""

import tkinter as tk
from tkinter import ttk, messagebox
from utils import create_tooltip

# Import admin components
from admin_user_manager import UserManager
from admin_company_manager import CompanyManager
from admin_coi_manager import COIManager

class AdminScreen(ttk.Frame):
    def __init__(self, parent, model, data_manager, current_user, back_callback):
        super().__init__(parent)
        self.parent = parent
        self.model = model
        self.data_manager = data_manager
        self.current_user = current_user
        self.back_callback = back_callback
        
        # Check if user has admin privileges
        user_info = self.model.users.get(self.current_user, {})
        if user_info.get('role') != 'administrator':
            messagebox.showerror("Access Denied", 
                               "You do not have administrator privileges.")
            self.back_callback()
            return
        
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
    
    def create_widgets(self):
        """Create the widgets for the admin screen"""
        # Header with back button
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        back_button = ttk.Button(header_frame, text="← Back to Dashboard", 
                                command=self.back_callback)
        back_button.pack(side=tk.LEFT)
        
        title_label = ttk.Label(header_frame, text="Administrator Panel", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(side=tk.LEFT, padx=20)
        
        # Create notebook for different admin functions
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # User Management tab
        user_tab = ttk.Frame(notebook)
        notebook.add(user_tab, text="User Management")
        self.user_manager = UserManager(user_tab, self.model, self.data_manager)
        
        # Company Management tab
        company_tab = ttk.Frame(notebook)
        notebook.add(company_tab, text="Company Management")
        self.company_manager = CompanyManager(company_tab, self.model, self.data_manager)
        
        # COI Class Management tab
        coi_tab = ttk.Frame(notebook)
        notebook.add(coi_tab, text="COI Class Management")
        self.coi_manager = COIManager(coi_tab, self.model, self.data_manager)
        
        # System Information tab
        system_tab = ttk.Frame(notebook)
        notebook.add(system_tab, text="System Information")
        self.create_system_info_tab(system_tab)
    
    def create_system_info_tab(self, parent):
        """Create the System Information tab"""
        # Create frame for system information
        info_frame = ttk.Frame(parent)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # System statistics
        stats_frame = ttk.LabelFrame(info_frame, text="System Statistics")
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Count entities
        num_users = len(self.model.users)
        num_companies = len(self.model.companies)
        num_coi_classes = len(self.model.coi_classes)
        num_access_logs = len(self.model.access_logs)
        
        # Display statistics
        ttk.Label(stats_frame, text=f"Total Users: {num_users}").pack(anchor=tk.W, padx=10, pady=5)
        ttk.Label(stats_frame, text=f"Total Companies: {num_companies}").pack(anchor=tk.W, padx=10, pady=5)
        ttk.Label(stats_frame, text=f"Total COI Classes: {num_coi_classes}").pack(anchor=tk.W, padx=10, pady=5)
        ttk.Label(stats_frame, text=f"Total Access Logs: {num_access_logs}").pack(anchor=tk.W, padx=10, pady=5)
        
        # System actions
        actions_frame = ttk.LabelFrame(info_frame, text="System Actions")
        actions_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Reset all user histories
        reset_button = ttk.Button(actions_frame, text="Reset All User Access Histories", 
                                 command=self.reset_all_histories)
        reset_button.pack(padx=10, pady=10, fill=tk.X)
        create_tooltip(reset_button, "Reset access history for all users")
        
        # Clear all access logs
        clear_logs_button = ttk.Button(actions_frame, text="Clear All Access Logs", 
                                      command=self.clear_access_logs)
        clear_logs_button.pack(padx=10, pady=10, fill=tk.X)
        create_tooltip(clear_logs_button, "Delete all access log entries")
        
        # Reinitialize sample data
        reinit_button = ttk.Button(actions_frame, text="Reinitialize Sample Data", 
                                  command=self.reinitialize_data)
        reinit_button.pack(padx=10, pady=10, fill=tk.X)
        create_tooltip(reinit_button, "Reset the system to its initial state with sample data")
    
    def reset_all_histories(self):
        """Reset access history for all users"""
        if messagebox.askyesno("Confirm Reset", 
                              "Are you sure you want to reset ALL user access histories?"):
            for user_id in self.model.user_access_history:
                self.model.reset_user_history(user_id)
            messagebox.showinfo("Reset Complete", "All user access histories have been reset.")
    
    def clear_access_logs(self):
        """Clear all access logs"""
        if messagebox.askyesno("Confirm Clear", 
                              "Are you sure you want to clear ALL access logs?"):
            self.model.access_logs = []
            messagebox.showinfo("Clear Complete", "All access logs have been cleared.")
    
    def reinitialize_data(self):
        """Reinitialize the sample data"""
        if messagebox.askyesno("Confirm Reinitialization", 
                              "Are you sure you want to reinitialize all sample data? " +
                              "This will reset the entire system."):
            # Reset the model
            self.model.coi_classes = {}
            self.model.user_access_history = {}
            self.model.access_logs = []
            self.model.companies = {}
            self.model.users = {}
            
            # Reinitialize sample data
            self.data_manager.initialize_sample_data()
            
            messagebox.showinfo("Reinitialization Complete", 
                               "The system has been reinitialized with sample data.")
