"""
Login Screen for Chinese Wall Model Demonstration
"""

import tkinter as tk
from tkinter import ttk, messagebox
from utils import create_tooltip, center_window, create_info_box, explain_chinese_wall

class LoginScreen(ttk.Frame):
    def __init__(self, parent, model, login_callback):
        super().__init__(parent)
        self.parent = parent
        self.model = model
        self.login_callback = login_callback
        
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
    
    def create_widgets(self):
        """Create the widgets for the login screen"""
        # Main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="Chinese Wall Model Demonstration", 
                               font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Login frame
        login_frame = ttk.LabelFrame(main_frame, text="User Login")
        login_frame.pack(padx=50, pady=20, ipadx=20, ipady=10)
        
        # User selection
        ttk.Label(login_frame, text="Select User:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        
        # Get all users
        self.users = self.model.users
        user_options = [(user_id, f"{info['name']} ({info['role']})") 
                        for user_id, info in self.users.items()]
        
        # User combobox
        self.user_var = tk.StringVar()
        self.user_combobox = ttk.Combobox(login_frame, textvariable=self.user_var, 
                                         state="readonly", width=30)
        self.user_combobox['values'] = [option[1] for option in user_options]
        self.user_combobox.grid(row=0, column=1, padx=10, pady=10)
        self.user_combobox.current(0)
        
        # Store the mapping of display names to user IDs
        self.user_id_map = {option[1]: option[0] for option in user_options}
        
        # Login button
        login_button = ttk.Button(login_frame, text="Login", command=self.login)
        login_button.grid(row=1, column=0, columnspan=2, pady=20)
        
        # Information section
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Introduction to Chinese Wall Model
        intro_label = ttk.Label(info_frame, text="Introduction to Chinese Wall Model", 
                               font=('Arial', 14, 'bold'))
        intro_label.pack(anchor=tk.W, pady=(0, 10))
        
        explanation = explain_chinese_wall()
        explanation_text = tk.Text(info_frame, wrap=tk.WORD, height=15, width=80)
        explanation_text.insert(tk.END, explanation)
        explanation_text.config(state=tk.DISABLED)
        explanation_text.pack(fill=tk.BOTH, expand=True)
        
        # Instructions
        instruction_frame = ttk.LabelFrame(main_frame, text="Instructions")
        instruction_frame.pack(fill=tk.X, padx=50, pady=20)
        
        instructions = """
1. Select a user from the dropdown menu and click 'Login'
2. Explore the system by attempting to access different company datasets
3. Notice how the Chinese Wall Model prevents access to conflicting datasets
4. Use the reporting features to analyze access patterns
5. Reset user history to start fresh with a new simulation
        """
        
        instruction_text = tk.Text(instruction_frame, wrap=tk.WORD, height=8, width=80)
        instruction_text.insert(tk.END, instructions)
        instruction_text.config(state=tk.DISABLED)
        instruction_text.pack(padx=10, pady=10)
    
    def login(self):
        """Handle login button click"""
        selected_user_display = self.user_var.get()
        if not selected_user_display:
            messagebox.showerror("Error", "Please select a user")
            return
        
        user_id = self.user_id_map[selected_user_display]
        self.login_callback(user_id)
