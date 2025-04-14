"""
Login Screen for Chinese Wall Model Demonstration
"""

import tkinter as tk
from tkinter import ttk, messagebox
from utils import (create_tooltip, create_info_box, create_card, 
                  create_badge, center_window, create_notification)
import random

class LoginScreen(ttk.Frame):
    def __init__(self, parent, model, login_callback):
        super().__init__(parent)
        self.parent = parent
        self.model = model
        self.login_callback = login_callback
        
        # Set up variables
        self.selected_user = tk.StringVar()
        
        # Configure the frame
        self.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create widgets
        self.create_widgets()
    
    def create_widgets(self):
        """Create the widgets for the login screen"""
        # Main container with two columns
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left column - Login form
        left_frame = ttk.Frame(main_container)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Right column - Information
        right_frame = ttk.Frame(main_container)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create the content for each column
        self.create_login_form(left_frame)
        self.create_info_panel(right_frame)
    
    def create_login_form(self, parent):
        """Create the login form"""
        # Header
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Logo placeholder (could be replaced with an actual image)
        logo_frame = tk.Frame(header_frame, bg="#1976d2", width=60, height=60)
        logo_frame.pack(side=tk.LEFT, padx=(0, 15))
        logo_frame.pack_propagate(False)
        
        logo_text = tk.Label(logo_frame, text="CW", font=('Arial', 24, 'bold'), 
                            fg="white", bg="#1976d2")
        logo_text.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        
        title_label = ttk.Label(title_frame, text="Chinese Wall Security Model", 
                               font=('Arial', 18, 'bold'))
        title_label.pack(anchor=tk.W)
        
        subtitle_label = ttk.Label(title_frame, text="Demonstration Application", 
                                  font=('Arial', 12))
        subtitle_label.pack(anchor=tk.W)
        
        # Login card
        login_card = create_card(parent, "User Login", title_bg="#e3f2fd")
        
        # Login form content
        login_content = tk.Frame(login_card, bg="white")
        login_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # User selection
        user_label = ttk.Label(login_content, text="Select User:", 
                              font=('Arial', 11, 'bold'))
        user_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Create a frame for the user selection options
        users_frame = tk.Frame(login_content, bg="white")
        users_frame.pack(fill=tk.X, pady=10)
        
        # Group users by role
        users_by_role = {}
        for user_id, user_info in self.model.users.items():
            role = user_info['role']
            if role not in users_by_role:
                users_by_role[role] = []
            users_by_role[role].append((user_id, user_info))
        
        # Role colors for badges
        role_colors = {
            'administrator': ('#d32f2f', 'white'),  # Red for admin
            'analyst': ('#1976d2', 'white'),  # Blue for analyst
            'auditor': ('#388e3c', 'white')   # Green for auditor
        }
        
        # Create a section for each role
        for role, users in users_by_role.items():
            # Role header with badge
            role_frame = tk.Frame(users_frame, bg="white")
            role_frame.pack(fill=tk.X, pady=5)
            
            bg_color, fg_color = role_colors.get(role, ('#757575', 'white'))
            role_badge = create_badge(role_frame, role.capitalize(), 
                                     bg_color=bg_color, fg_color=fg_color)
            role_badge.pack(anchor=tk.W, pady=(0, 5))
            
            # Create user selection options
            for user_id, user_info in users:
                user_option = ttk.Radiobutton(
                    users_frame, 
                    text=f"{user_info['name']} ({user_id})",
                    value=user_id,
                    variable=self.selected_user
                )
                user_option.pack(anchor=tk.W, padx=15, pady=2)
                
                # Add tooltip with user description
                tooltip_text = f"Role: {role.capitalize()}\nID: {user_id}"
                if 'description' in user_info:
                    tooltip_text += f"\n\n{user_info['description']}"
                create_tooltip(user_option, tooltip_text)
        
        # Login button
        button_frame = tk.Frame(login_content, bg="white")
        button_frame.pack(fill=tk.X, pady=20)
        
        login_button = ttk.Button(
            button_frame, 
            text="Login",
            command=self.login,
            style="Accent.TButton"  # Using the accent style defined in gui_app.py
        )
        login_button.pack(side=tk.RIGHT, padx=5)
        
        # Random user button for quick testing
        random_button = ttk.Button(
            button_frame,
            text="Random User",
            command=self.select_random_user
        )
        random_button.pack(side=tk.RIGHT, padx=5)
        create_tooltip(random_button, "Select a random user for quick testing")
    
    def create_info_panel(self, parent):
        """Create the information panel"""
        # Chinese Wall explanation card
        explanation_card = create_card(parent, "About Chinese Wall Security Model", 
                                      title_bg="#e3f2fd")
        
        # Explanation content
        explanation_content = tk.Frame(explanation_card, bg="white")
        explanation_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        explanation_text = """
The Chinese Wall security model prevents conflicts of interest by dynamically restricting access based on a user's access history.

Key features:
• Users can initially access any company's data
• Once a user accesses data from a company, they cannot access data from competing companies
• Companies are grouped into Conflict of Interest (COI) classes
• Access rights are determined based on the user's access history

This demonstration allows you to:
• Log in as different users with various roles
• Access company data within COI classes
• Experience the Chinese Wall security restrictions
• Generate reports and visualizations of access patterns
• Administer users, companies, and COI classes (admin only)
        """
        
        explanation_label = tk.Label(explanation_content, text=explanation_text,
                                    justify=tk.LEFT, wraplength=350, bg="white")
        explanation_label.pack(fill=tk.X, pady=5)
        
        # Instructions card
        instructions_card = create_card(parent, "Instructions", title_bg="#e3f2fd")
        
        # Instructions content
        instructions_content = tk.Frame(instructions_card, bg="white")
        instructions_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        instructions_text = """
1. Select a user from the list on the left
2. Click "Login" to enter the application
3. On the main dashboard, you'll see companies grouped by sector
4. Try accessing data from different companies
5. Notice how your access rights change based on your history
6. Use the navigation buttons to explore reports and help
7. Administrators can access the admin panel to manage the system
        """
        
        instructions_label = tk.Label(instructions_content, text=instructions_text,
                                     justify=tk.LEFT, wraplength=350, bg="white")
        instructions_label.pack(fill=tk.X, pady=5)
        
        # Version info at the bottom
        version_frame = tk.Frame(parent, bg="#f5f5f5")
        version_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
        
        version_label = tk.Label(version_frame, text="Chinese Wall Demo v1.0", 
                                font=('Arial', 8), fg="#757575", bg="#f5f5f5")
        version_label.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def login(self):
        """Handle the login button click"""
        selected_user = self.selected_user.get()
        
        if not selected_user:
            create_notification(self, "Please select a user to continue", "warning")
            return
        
        # Get user info for the notification
        user_info = self.model.users[selected_user]
        user_name = user_info['name']
        user_role = user_info['role'].capitalize()
        
        # Show login notification
        create_notification(self, f"Logging in as {user_name} ({user_role})", "success")
        
        # Call the login callback with the selected user
        self.login_callback(selected_user)
    
    def select_random_user(self):
        """Select a random user for quick testing"""
        user_ids = list(self.model.users.keys())
        random_user = random.choice(user_ids)
        
        # Set the selected user
        self.selected_user.set(random_user)
        
        # Show notification
        user_name = self.model.users[random_user]['name']
        create_notification(self, f"Selected random user: {user_name}", "info")
