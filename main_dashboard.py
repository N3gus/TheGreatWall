"""
Main Dashboard for Chinese Wall Model Demonstration
"""

import tkinter as tk
from tkinter import ttk, messagebox
from utils import create_tooltip, create_scrollable_frame, create_section_header, format_access_result

class MainDashboard(ttk.Frame):
    def __init__(self, parent, model, data_manager, current_user, 
                 logout_callback, show_report_screen, show_admin_screen, show_help_screen):
        super().__init__(parent)
        self.parent = parent
        self.model = model
        self.data_manager = data_manager
        self.current_user = current_user
        self.logout_callback = logout_callback
        self.show_report_screen = show_report_screen
        self.show_admin_screen = show_admin_screen
        self.show_help_screen = show_help_screen
        
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
    
    def create_widgets(self):
        """Create the widgets for the main dashboard"""
        # Main container with two columns
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left column (70% width) - Company data access
        left_frame = ttk.Frame(main_container)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right column (30% width) - User info and controls
        right_frame = ttk.Frame(main_container)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=5, pady=5, ipadx=10)
        
        # Create the content for each column
        self.create_left_column(left_frame)
        self.create_right_column(right_frame)
    
    def create_left_column(self, parent):
        """Create the content for the left column (company data access)"""
        # Header
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        header_label = ttk.Label(header_frame, text="Company Data Access", 
                                font=('Arial', 16, 'bold'))
        header_label.pack(side=tk.LEFT)
        
        # Notebook for organizing companies by COI class
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create a tab for each COI class
        for coi_class_id in self.model.coi_classes:
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=f"{coi_class_id.capitalize()} Sector")
            
            # Create scrollable frame for company cards
            scrollable_frame = create_scrollable_frame(tab)
            
            # Get companies in this COI class
            companies_in_class = {company_id: company_info 
                                 for company_id, company_info in self.model.companies.items() 
                                 if company_info['coi_class'] == coi_class_id}
            
            # Create a card for each company
            for company_id, company_info in companies_in_class.items():
                self.create_company_card(scrollable_frame, company_id, company_info)
        
        # Access log section
        log_frame = ttk.LabelFrame(parent, text="Recent Access Log")
        log_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create scrollable text widget for logs
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, height=8)
        self.log_text.pack(fill=tk.X, padx=5, pady=5)
        
        # Add scrollbar to log text
        log_scrollbar = ttk.Scrollbar(self.log_text, command=self.log_text.yview)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=log_scrollbar.set)
        
        # Disable text editing
        self.log_text.config(state=tk.DISABLED)
    
    def create_right_column(self, parent):
        """Create the content for the right column (user info and controls)"""
        # User information
        user_frame = ttk.LabelFrame(parent, text="User Information")
        user_frame.pack(fill=tk.X, padx=5, pady=5)
        
        user_info = self.model.users[self.current_user]
        
        ttk.Label(user_frame, text=f"Name: {user_info['name']}").pack(anchor=tk.W, padx=10, pady=2)
        ttk.Label(user_frame, text=f"Role: {user_info['role'].capitalize()}").pack(anchor=tk.W, padx=10, pady=2)
        ttk.Label(user_frame, text=f"ID: {self.current_user}").pack(anchor=tk.W, padx=10, pady=2)
        
        # Access history
        history_frame = ttk.LabelFrame(parent, text="Access History")
        history_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Get user's access history
        access_history = self.model.user_access_history.get(self.current_user, {})
        
        if access_history:
            for company_id in access_history:
                company_name = self.model.companies[company_id]['name']
                ttk.Label(history_frame, text=f"• {company_name}").pack(anchor=tk.W, padx=10, pady=2)
        else:
            ttk.Label(history_frame, text="No access history").pack(anchor=tk.W, padx=10, pady=2)
        
        # Reset history button
        reset_button = ttk.Button(history_frame, text="Reset Access History", 
                                 command=self.reset_access_history)
        reset_button.pack(padx=10, pady=10)
        create_tooltip(reset_button, "Reset your access history to start fresh")
        
        # Navigation buttons
        nav_frame = ttk.LabelFrame(parent, text="Navigation")
        nav_frame.pack(fill=tk.X, padx=5, pady=5)
        
        report_button = ttk.Button(nav_frame, text="Access Reports", 
                                  command=self.show_report_screen)
        report_button.pack(fill=tk.X, padx=10, pady=5)
        create_tooltip(report_button, "View detailed access reports and analytics")
        
        # Only show admin button for admin users
        if user_info['role'] == 'administrator':
            admin_button = ttk.Button(nav_frame, text="Admin Panel", 
                                     command=self.show_admin_screen)
            admin_button.pack(fill=tk.X, padx=10, pady=5)
            create_tooltip(admin_button, "Access administrative functions")
        
        help_button = ttk.Button(nav_frame, text="Help & Information", 
                               command=self.show_help_screen)
        help_button.pack(fill=tk.X, padx=10, pady=5)
        create_tooltip(help_button, "Learn more about the Chinese Wall Model")
        
        # Logout button at the bottom
        logout_frame = ttk.Frame(parent)
        logout_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=20)
        
        logout_button = ttk.Button(logout_frame, text="Logout", 
                                  command=self.logout_callback)
        logout_button.pack(fill=tk.X, padx=10, pady=5)
    
    def create_company_card(self, parent, company_id, company_info):
        """Create a card for a company with its data objects"""
        card_frame = ttk.LabelFrame(parent, text=company_info['name'])
        card_frame.pack(fill=tk.X, padx=10, pady=10, ipadx=5, ipady=5)
        
        # Company information
        info_frame = ttk.Frame(card_frame)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(info_frame, text=f"ID: {company_id}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Sector: {company_info['coi_class'].capitalize()}").pack(anchor=tk.W)
        
        # Check if user can access this company
        can_access, reason = self.model.can_access(self.current_user, company_id)
        
        # Access status
        status_label = ttk.Label(info_frame, 
                                text=f"Status: {'Accessible' if can_access else 'Restricted'}")
        status_label.pack(anchor=tk.W)
        
        # Data objects section
        if can_access:
            objects_frame = ttk.LabelFrame(card_frame, text="Available Data")
            objects_frame.pack(fill=tk.X, padx=5, pady=5)
            
            # Get company objects
            company_objects = self.model.get_company_objects(company_id)
            
            for object_id, object_data in company_objects.items():
                obj_frame = ttk.Frame(objects_frame)
                obj_frame.pack(fill=tk.X, padx=5, pady=2)
                
                ttk.Label(obj_frame, text=object_id, width=20).pack(side=tk.LEFT)
                
                access_button = ttk.Button(obj_frame, text="Access", 
                                         command=lambda cid=company_id, oid=object_id: 
                                         self.attempt_access(cid, oid))
                access_button.pack(side=tk.RIGHT, padx=5)
        else:
            # Show reason for restriction
            restriction_label = ttk.Label(card_frame, text=f"Reason: {reason}", 
                                        foreground="red")
            restriction_label.pack(anchor=tk.W, padx=5, pady=5)
    
    def attempt_access(self, company_id, object_id):
        """Attempt to access a company's data object"""
        # Get current timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Attempt access
        access_granted, reason = self.data_manager.simulate_access_attempt(
            self.current_user, company_id, object_id)
        
        # Show result in message box
        company_name = self.model.companies[company_id]['name']
        messagebox.showinfo(
            "Access Attempt", 
            f"Attempting to access '{object_id}' from {company_name}:\n\n" +
            format_access_result(access_granted, reason)
        )
        
        # Add to log
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, 
                           f"[{timestamp}] {company_name} - {object_id}: " +
                           format_access_result(access_granted, reason) + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # Refresh the dashboard to reflect changes
        self.refresh()
    
    def reset_access_history(self):
        """Reset the user's access history"""
        if messagebox.askyesno("Confirm Reset", 
                              "Are you sure you want to reset your access history? " +
                              "This will allow you to access any company again."):
            self.model.reset_user_history(self.current_user)
            messagebox.showinfo("Reset Complete", 
                               "Your access history has been reset. " +
                               "You can now access any company.")
            self.refresh()
    
    def refresh(self):
        """Refresh the dashboard to reflect changes"""
        # Destroy the current frame
        for widget in self.winfo_children():
            widget.destroy()
        
        # Recreate the widgets
        self.create_widgets()
