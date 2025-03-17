"""
User Manager Component for Admin Screen
Handles user management functionality
"""

import tkinter as tk
from tkinter import ttk, messagebox
from utils import create_tooltip, create_scrollable_frame

class UserManager(ttk.Frame):
    def __init__(self, parent, model, data_manager):
        super().__init__(parent)
        self.parent = parent
        self.model = model
        self.data_manager = data_manager
        
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
    
    def create_widgets(self):
        """Create the widgets for user management"""
        # Split into two panels
        panel_frame = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        panel_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - User list
        left_frame = ttk.Frame(panel_frame)
        panel_frame.add(left_frame, weight=1)
        
        # Right panel - User details/edit
        right_frame = ttk.Frame(panel_frame)
        panel_frame.add(right_frame, weight=2)
        
        # Create the content for each panel
        self.create_user_list(left_frame)
        self.create_user_details(right_frame)
    
    def create_user_list(self, parent):
        """Create the user list panel"""
        # Header with title and add button
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(header_frame, text="Users", font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        
        add_button = ttk.Button(header_frame, text="Add User", command=self.add_user)
        add_button.pack(side=tk.RIGHT)
        
        # Create a frame for the user list
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create a treeview for the user list
        columns = ('id', 'name', 'role')
        self.user_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Define column headings
        self.user_tree.heading('id', text='ID')
        self.user_tree.heading('name', text='Name')
        self.user_tree.heading('role', text='Role')
        
        # Define column widths
        self.user_tree.column('id', width=80)
        self.user_tree.column('name', width=150)
        self.user_tree.column('role', width=100)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.user_tree.yview)
        self.user_tree.configure(yscroll=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.user_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.user_tree.bind('<<TreeviewSelect>>', self.on_user_select)
        
        # Populate the user list
        self.refresh_user_list()
    
    def create_user_details(self, parent):
        """Create the user details/edit panel"""
        # Frame for user details
        self.details_frame = ttk.LabelFrame(parent, text="User Details")
        self.details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initially show a message to select a user
        self.select_label = ttk.Label(self.details_frame, 
                                     text="Select a user from the list or click 'Add User'")
        self.select_label.pack(padx=20, pady=20)
        
        # Create variables for user details
        self.user_id_var = tk.StringVar()
        self.user_name_var = tk.StringVar()
        self.user_role_var = tk.StringVar()
        
        # Create the edit form (initially hidden)
        self.edit_frame = ttk.Frame(self.details_frame)
        
        # User ID field
        id_frame = ttk.Frame(self.edit_frame)
        id_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(id_frame, text="User ID:", width=15).pack(side=tk.LEFT)
        self.id_entry = ttk.Entry(id_frame, textvariable=self.user_id_var)
        self.id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # User Name field
        name_frame = ttk.Frame(self.edit_frame)
        name_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(name_frame, text="Name:", width=15).pack(side=tk.LEFT)
        self.name_entry = ttk.Entry(name_frame, textvariable=self.user_name_var)
        self.name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # User Role field
        role_frame = ttk.Frame(self.edit_frame)
        role_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(role_frame, text="Role:", width=15).pack(side=tk.LEFT)
        
        roles = ["standard", "consultant", "analyst", "manager", "auditor", "administrator"]
        self.role_combobox = ttk.Combobox(role_frame, textvariable=self.user_role_var, 
                                         values=roles, state="readonly")
        self.role_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.edit_frame)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Save button
        self.save_button = ttk.Button(buttons_frame, text="Save", command=self.save_user)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        # Delete button
        self.delete_button = ttk.Button(buttons_frame, text="Delete", command=self.delete_user)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_button = ttk.Button(buttons_frame, text="Cancel", command=self.cancel_edit)
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Access history section
        self.history_frame = ttk.LabelFrame(parent, text="Access History")
        self.history_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)
        
        # Initially hide the history frame
        self.history_content = ttk.Frame(self.history_frame)
        
        # Reset history button
        self.reset_button = ttk.Button(self.history_content, text="Reset Access History", 
                                      command=self.reset_user_history)
        self.reset_button.pack(side=tk.BOTTOM, padx=10, pady=10)
    
    def refresh_user_list(self):
        """Refresh the user list"""
        # Clear the current list
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        
        # Add all users to the list
        for user_id, user_info in self.model.users.items():
            self.user_tree.insert('', tk.END, values=(user_id, user_info['name'], user_info['role']))
    
    def on_user_select(self, event):
        """Handle user selection in the treeview"""
        # Get the selected item
        selected_items = self.user_tree.selection()
        if not selected_items:
            return
        
        # Get the user ID from the selected item
        item = selected_items[0]
        user_id = self.user_tree.item(item, 'values')[0]
        
        # Get the user info
        user_info = self.model.users.get(user_id)
        if not user_info:
            return
        
        # Hide the select label
        self.select_label.pack_forget()
        
        # Set the user details
        self.user_id_var.set(user_id)
        self.user_name_var.set(user_info['name'])
        self.user_role_var.set(user_info['role'])
        
        # Show the edit form
        self.edit_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Disable the ID field for existing users
        self.id_entry.config(state="disabled")
        
        # Show the access history
        self.show_access_history(user_id)
    
    def show_access_history(self, user_id):
        """Show the user's access history"""
        # Clear the current history content
        for widget in self.history_content.winfo_children():
            if widget != self.reset_button:
                widget.destroy()
        
        # Get the user's access history
        access_history = self.model.user_access_history.get(user_id, {})
        
        if access_history:
            # Create a frame for the history list
            history_list = ttk.Frame(self.history_content)
            history_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Add a label for each accessed company
            ttk.Label(history_list, text="Companies Accessed:", 
                     font=('Arial', 10, 'bold')).pack(anchor=tk.W)
            
            for company_id in access_history:
                company_name = self.model.companies[company_id]['name']
                company_coi = self.model.companies[company_id]['coi_class']
                ttk.Label(history_list, 
                         text=f"• {company_name} (COI Class: {company_coi})").pack(anchor=tk.W, padx=10, pady=2)
        else:
            # Show a message if no history
            ttk.Label(self.history_content, 
                     text="No access history for this user").pack(padx=20, pady=20)
        
        # Show the history frame and content
        self.history_content.pack(fill=tk.BOTH, expand=True)
        self.history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def add_user(self):
        """Add a new user"""
        # Hide the select label
        self.select_label.pack_forget()
        
        # Clear the user details
        self.user_id_var.set("")
        self.user_name_var.set("")
        self.user_role_var.set("standard")
        
        # Enable the ID field for new users
        self.id_entry.config(state="normal")
        
        # Show the edit form
        self.edit_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Hide the history frame
        self.history_frame.pack_forget()
    
    def save_user(self):
        """Save the user details"""
        # Get the user details
        user_id = self.user_id_var.get()
        user_name = self.user_name_var.get()
        user_role = self.user_role_var.get()
        
        # Validate the input
        if not user_id or not user_name or not user_role:
            messagebox.showerror("Error", "All fields are required")
            return
        
        # Check if this is a new user or an update
        if user_id in self.model.users:
            # Update existing user
            self.model.users[user_id]['name'] = user_name
            self.model.users[user_id]['role'] = user_role
            messagebox.showinfo("Success", f"User '{user_name}' updated successfully")
        else:
            # Add new user
            success = self.data_manager.add_new_user(user_id, user_name, user_role)
            if success:
                messagebox.showinfo("Success", f"User '{user_name}' added successfully")
            else:
                messagebox.showerror("Error", f"Failed to add user '{user_name}'")
        
        # Refresh the user list
        self.refresh_user_list()
        
        # Reset the form
        self.cancel_edit()
    
    def delete_user(self):
        """Delete the selected user"""
        user_id = self.user_id_var.get()
        user_name = self.user_name_var.get()
        
        if not user_id or user_id not in self.model.users:
            messagebox.showerror("Error", "No valid user selected")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", 
                                  f"Are you sure you want to delete user '{user_name}'?"):
            return
        
        # Delete the user
        del self.model.users[user_id]
        if user_id in self.model.user_access_history:
            del self.model.user_access_history[user_id]
        
        messagebox.showinfo("Success", f"User '{user_name}' deleted successfully")
        
        # Refresh the user list
        self.refresh_user_list()
        
        # Reset the form
        self.cancel_edit()
    
    def cancel_edit(self):
        """Cancel editing and reset the form"""
        # Hide the edit form
        self.edit_frame.pack_forget()
        
        # Hide the history frame
        self.history_frame.pack_forget()
        
        # Show the select label
        self.select_label.pack(padx=20, pady=20)
        
        # Clear the selection in the treeview
        self.user_tree.selection_remove(self.user_tree.selection())
    
    def reset_user_history(self):
        """Reset the selected user's access history"""
        user_id = self.user_id_var.get()
        user_name = self.user_name_var.get()
        
        if not user_id or user_id not in self.model.users:
            messagebox.showerror("Error", "No valid user selected")
            return
        
        # Confirm reset
        if not messagebox.askyesno("Confirm Reset", 
                                  f"Are you sure you want to reset access history for '{user_name}'?"):
            return
        
        # Reset the user's history
        self.model.reset_user_history(user_id)
        
        messagebox.showinfo("Success", f"Access history for '{user_name}' has been reset")
        
        # Update the history display
        self.show_access_history(user_id)
