"""
COI Class Manager Component for Admin Screen
Handles Conflict of Interest class management functionality
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from utils import create_tooltip, create_scrollable_frame

class COIManager(ttk.Frame):
    def __init__(self, parent, model, data_manager):
        super().__init__(parent)
        self.parent = parent
        self.model = model
        self.data_manager = data_manager
        
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
    
    def create_widgets(self):
        """Create the widgets for COI class management"""
        # Split into two panels
        panel_frame = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        panel_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - COI class list
        left_frame = ttk.Frame(panel_frame)
        panel_frame.add(left_frame, weight=1)
        
        # Right panel - COI class details/edit
        right_frame = ttk.Frame(panel_frame)
        panel_frame.add(right_frame, weight=2)
        
        # Create the content for each panel
        self.create_coi_list(left_frame)
        self.create_coi_details(right_frame)
    
    def create_coi_list(self, parent):
        """Create the COI class list panel"""
        # Header with title and add button
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(header_frame, text="COI Classes", font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        
        add_button = ttk.Button(header_frame, text="Add COI Class", command=self.add_coi_class)
        add_button.pack(side=tk.RIGHT)
        
        # Create a frame for the COI class list
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create a treeview for the COI class list
        columns = ('id', 'companies')
        self.coi_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Define column headings
        self.coi_tree.heading('id', text='COI Class ID')
        self.coi_tree.heading('companies', text='Companies')
        
        # Define column widths
        self.coi_tree.column('id', width=100)
        self.coi_tree.column('companies', width=200)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.coi_tree.yview)
        self.coi_tree.configure(yscroll=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.coi_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.coi_tree.bind('<<TreeviewSelect>>', self.on_coi_select)
        
        # Populate the COI class list
        self.refresh_coi_list()
    
    def create_coi_details(self, parent):
        """Create the COI class details/edit panel"""
        # Frame for COI class details
        self.details_frame = ttk.LabelFrame(parent, text="COI Class Details")
        self.details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initially show a message to select a COI class
        self.select_label = ttk.Label(self.details_frame, 
                                     text="Select a COI class from the list or click 'Add COI Class'")
        self.select_label.pack(padx=20, pady=20)
        
        # Create variables for COI class details
        self.coi_id_var = tk.StringVar()
        
        # Create the edit form (initially hidden)
        self.edit_frame = ttk.Frame(self.details_frame)
        
        # COI Class ID field
        id_frame = ttk.Frame(self.edit_frame)
        id_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(id_frame, text="COI Class ID:", width=15).pack(side=tk.LEFT)
        self.id_entry = ttk.Entry(id_frame, textvariable=self.coi_id_var)
        self.id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Description field
        desc_frame = ttk.Frame(self.edit_frame)
        desc_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(desc_frame, text="Description:", width=15).pack(side=tk.LEFT)
        
        # Description is not stored in the model, so we'll just show a text field
        self.desc_text = tk.Text(desc_frame, height=3, width=30)
        self.desc_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.edit_frame)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Save button
        self.save_button = ttk.Button(buttons_frame, text="Save", command=self.save_coi_class)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        # Delete button
        self.delete_button = ttk.Button(buttons_frame, text="Delete", command=self.delete_coi_class)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_button = ttk.Button(buttons_frame, text="Cancel", command=self.cancel_edit)
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Companies section
        self.companies_frame = ttk.LabelFrame(parent, text="Companies in this COI Class")
        self.companies_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initially hide the companies frame
        self.companies_content = ttk.Frame(self.companies_frame)
        
        # Create a frame for the companies list
        companies_list_frame = ttk.Frame(self.companies_content)
        companies_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create a treeview for the companies list
        columns = ('id', 'name', 'objects')
        self.companies_tree = ttk.Treeview(companies_list_frame, columns=columns, show='headings')
        
        # Define column headings
        self.companies_tree.heading('id', text='ID')
        self.companies_tree.heading('name', text='Name')
        self.companies_tree.heading('objects', text='Objects')
        
        # Define column widths
        self.companies_tree.column('id', width=80)
        self.companies_tree.column('name', width=150)
        self.companies_tree.column('objects', width=100)
        
        # Add a scrollbar
        companies_scrollbar = ttk.Scrollbar(companies_list_frame, orient=tk.VERTICAL, 
                                           command=self.companies_tree.yview)
        self.companies_tree.configure(yscroll=companies_scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.companies_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        companies_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def refresh_coi_list(self):
        """Refresh the COI class list"""
        # Clear the current list
        for item in self.coi_tree.get_children():
            self.coi_tree.delete(item)
        
        # Add all COI classes to the list
        for coi_class_id, companies in self.model.coi_classes.items():
            # Count companies in this COI class
            company_count = len(companies)
            company_text = f"{company_count} companies"
            
            self.coi_tree.insert('', tk.END, values=(coi_class_id, company_text))
    
    def on_coi_select(self, event):
        """Handle COI class selection in the treeview"""
        # Get the selected item
        selected_items = self.coi_tree.selection()
        if not selected_items:
            return
        
        # Get the COI class ID from the selected item
        item = selected_items[0]
        coi_class_id = self.coi_tree.item(item, 'values')[0]
        
        # Get the COI class info
        if coi_class_id not in self.model.coi_classes:
            return
        
        # Hide the select label
        self.select_label.pack_forget()
        
        # Set the COI class details
        self.coi_id_var.set(coi_class_id)
        
        # Set description (this is just for display, not stored in the model)
        self.desc_text.delete(1.0, tk.END)
        self.desc_text.insert(tk.END, f"Conflict of Interest Class for {coi_class_id.capitalize()} sector")
        
        # Show the edit form
        self.edit_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Disable the ID field for existing COI classes
        self.id_entry.config(state="disabled")
        
        # Show the companies in this COI class
        self.show_companies(coi_class_id)
    
    def show_companies(self, coi_class_id):
        """Show the companies in this COI class"""
        # Clear the current companies list
        for item in self.companies_tree.get_children():
            self.companies_tree.delete(item)
        
        # Get the companies in this COI class
        companies = self.model.coi_classes.get(coi_class_id, {})
        
        # Add all companies to the list
        for company_id, objects in companies.items():
            company_name = self.model.companies[company_id]['name']
            object_count = len(objects)
            
            self.companies_tree.insert('', tk.END, values=(company_id, company_name, f"{object_count} objects"))
        
        # Show the companies frame and content
        self.companies_content.pack(fill=tk.BOTH, expand=True)
        self.companies_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def add_coi_class(self):
        """Add a new COI class"""
        # Hide the select label
        self.select_label.pack_forget()
        
        # Clear the COI class details
        self.coi_id_var.set("")
        self.desc_text.delete(1.0, tk.END)
        
        # Enable the ID field for new COI classes
        self.id_entry.config(state="normal")
        
        # Show the edit form
        self.edit_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Hide the companies frame
        self.companies_frame.pack_forget()
    
    def save_coi_class(self):
        """Save the COI class details"""
        # Get the COI class details
        coi_class_id = self.coi_id_var.get()
        
        # Validate the input
        if not coi_class_id:
            messagebox.showerror("Error", "COI Class ID is required")
            return
        
        # Check if this is a new COI class or an update
        if coi_class_id in self.model.coi_classes:
            # Update existing COI class (nothing to update except ID, which we don't allow)
            messagebox.showinfo("Success", f"COI Class '{coi_class_id}' updated successfully")
        else:
            # Add new COI class
            success = self.data_manager.add_new_coi_class(coi_class_id, coi_class_id.capitalize())
            if success:
                messagebox.showinfo("Success", f"COI Class '{coi_class_id}' added successfully")
            else:
                messagebox.showerror("Error", f"Failed to add COI Class '{coi_class_id}'")
        
        # Refresh the COI class list
        self.refresh_coi_list()
        
        # Reset the form
        self.cancel_edit()
    
    def delete_coi_class(self):
        """Delete the selected COI class"""
        coi_class_id = self.coi_id_var.get()
        
        if not coi_class_id or coi_class_id not in self.model.coi_classes:
            messagebox.showerror("Error", "No valid COI class selected")
            return
        
        # Check if there are companies in this COI class
        companies = self.model.coi_classes.get(coi_class_id, {})
        if companies:
            messagebox.showerror("Error", 
                               f"Cannot delete COI Class '{coi_class_id}' because it contains companies. " +
                               "Move or delete the companies first.")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", 
                                  f"Are you sure you want to delete COI Class '{coi_class_id}'?"):
            return
        
        # Delete the COI class
        del self.model.coi_classes[coi_class_id]
        
        messagebox.showinfo("Success", f"COI Class '{coi_class_id}' deleted successfully")
        
        # Refresh the COI class list
        self.refresh_coi_list()
        
        # Reset the form
        self.cancel_edit()
    
    def cancel_edit(self):
        """Cancel editing and reset the form"""
        # Hide the edit form
        self.edit_frame.pack_forget()
        
        # Hide the companies frame
        self.companies_frame.pack_forget()
        
        # Show the select label
        self.select_label.pack(padx=20, pady=20)
        
        # Clear the selection in the treeview
        self.coi_tree.selection_remove(self.coi_tree.selection())
