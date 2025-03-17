"""
Company Manager Component for Admin Screen
Handles company management functionality
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from utils import create_tooltip, create_scrollable_frame

class CompanyManager(ttk.Frame):
    def __init__(self, parent, model, data_manager):
        super().__init__(parent)
        self.parent = parent
        self.model = model
        self.data_manager = data_manager
        
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
    
    def create_widgets(self):
        """Create the widgets for company management"""
        # Split into two panels
        panel_frame = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        panel_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Company list
        left_frame = ttk.Frame(panel_frame)
        panel_frame.add(left_frame, weight=1)
        
        # Right panel - Company details/edit
        right_frame = ttk.Frame(panel_frame)
        panel_frame.add(right_frame, weight=2)
        
        # Create the content for each panel
        self.create_company_list(left_frame)
        self.create_company_details(right_frame)
    
    def create_company_list(self, parent):
        """Create the company list panel"""
        # Header with title and add button
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(header_frame, text="Companies", font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        
        add_button = ttk.Button(header_frame, text="Add Company", command=self.add_company)
        add_button.pack(side=tk.RIGHT)
        
        # Create a frame for the company list
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create a treeview for the company list
        columns = ('id', 'name', 'coi_class')
        self.company_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Define column headings
        self.company_tree.heading('id', text='ID')
        self.company_tree.heading('name', text='Name')
        self.company_tree.heading('coi_class', text='COI Class')
        
        # Define column widths
        self.company_tree.column('id', width=80)
        self.company_tree.column('name', width=150)
        self.company_tree.column('coi_class', width=100)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.company_tree.yview)
        self.company_tree.configure(yscroll=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.company_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.company_tree.bind('<<TreeviewSelect>>', self.on_company_select)
        
        # Populate the company list
        self.refresh_company_list()
    
    def create_company_details(self, parent):
        """Create the company details/edit panel"""
        # Frame for company details
        self.details_frame = ttk.LabelFrame(parent, text="Company Details")
        self.details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initially show a message to select a company
        self.select_label = ttk.Label(self.details_frame, 
                                     text="Select a company from the list or click 'Add Company'")
        self.select_label.pack(padx=20, pady=20)
        
        # Create variables for company details
        self.company_id_var = tk.StringVar()
        self.company_name_var = tk.StringVar()
        self.company_coi_var = tk.StringVar()
        
        # Create the edit form (initially hidden)
        self.edit_frame = ttk.Frame(self.details_frame)
        
        # Company ID field
        id_frame = ttk.Frame(self.edit_frame)
        id_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(id_frame, text="Company ID:", width=15).pack(side=tk.LEFT)
        self.id_entry = ttk.Entry(id_frame, textvariable=self.company_id_var)
        self.id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Company Name field
        name_frame = ttk.Frame(self.edit_frame)
        name_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(name_frame, text="Name:", width=15).pack(side=tk.LEFT)
        self.name_entry = ttk.Entry(name_frame, textvariable=self.company_name_var)
        self.name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # COI Class field
        coi_frame = ttk.Frame(self.edit_frame)
        coi_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(coi_frame, text="COI Class:", width=15).pack(side=tk.LEFT)
        
        # Get all COI classes
        coi_classes = list(self.model.coi_classes.keys())
        self.coi_combobox = ttk.Combobox(coi_frame, textvariable=self.company_coi_var, 
                                        values=coi_classes, state="readonly")
        self.coi_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.edit_frame)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Save button
        self.save_button = ttk.Button(buttons_frame, text="Save", command=self.save_company)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        # Delete button
        self.delete_button = ttk.Button(buttons_frame, text="Delete", command=self.delete_company)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_button = ttk.Button(buttons_frame, text="Cancel", command=self.cancel_edit)
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Data Objects section
        self.objects_frame = ttk.LabelFrame(parent, text="Data Objects")
        self.objects_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initially hide the objects frame
        self.objects_content = ttk.Frame(self.objects_frame)
        
        # Header with add object button
        obj_header_frame = ttk.Frame(self.objects_content)
        obj_header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.add_object_button = ttk.Button(obj_header_frame, text="Add Data Object", 
                                           command=self.add_data_object)
        self.add_object_button.pack(side=tk.RIGHT)
        
        # Create a frame for the objects list
        obj_list_frame = ttk.Frame(self.objects_content)
        obj_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create a treeview for the objects list
        columns = ('id', 'data')
        self.objects_tree = ttk.Treeview(obj_list_frame, columns=columns, show='headings')
        
        # Define column headings
        self.objects_tree.heading('id', text='Object ID')
        self.objects_tree.heading('data', text='Data')
        
        # Define column widths
        self.objects_tree.column('id', width=100)
        self.objects_tree.column('data', width=300)
        
        # Add a scrollbar
        obj_scrollbar = ttk.Scrollbar(obj_list_frame, orient=tk.VERTICAL, command=self.objects_tree.yview)
        self.objects_tree.configure(yscroll=obj_scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.objects_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        obj_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event for objects
        self.objects_tree.bind('<<TreeviewSelect>>', self.on_object_select)
        
        # Add context menu for objects
        self.create_object_context_menu()
    
    def create_object_context_menu(self):
        """Create a context menu for the objects treeview"""
        self.object_menu = tk.Menu(self, tearoff=0)
        self.object_menu.add_command(label="Edit", command=self.edit_data_object)
        self.object_menu.add_command(label="Delete", command=self.delete_data_object)
        
        # Bind right-click to show the menu
        self.objects_tree.bind("<Button-3>", self.show_object_menu)
    
    def show_object_menu(self, event):
        """Show the context menu for objects"""
        # Select the item under the cursor
        item = self.objects_tree.identify_row(event.y)
        if item:
            self.objects_tree.selection_set(item)
            self.object_menu.post(event.x_root, event.y_root)
    
    def refresh_company_list(self):
        """Refresh the company list"""
        # Clear the current list
        for item in self.company_tree.get_children():
            self.company_tree.delete(item)
        
        # Add all companies to the list
        for company_id, company_info in self.model.companies.items():
            self.company_tree.insert('', tk.END, values=(
                company_id, 
                company_info['name'], 
                company_info['coi_class']
            ))
    
    def on_company_select(self, event):
        """Handle company selection in the treeview"""
        # Get the selected item
        selected_items = self.company_tree.selection()
        if not selected_items:
            return
        
        # Get the company ID from the selected item
        item = selected_items[0]
        company_id = self.company_tree.item(item, 'values')[0]
        
        # Get the company info
        company_info = self.model.companies.get(company_id)
        if not company_info:
            return
        
        # Hide the select label
        self.select_label.pack_forget()
        
        # Set the company details
        self.company_id_var.set(company_id)
        self.company_name_var.set(company_info['name'])
        self.company_coi_var.set(company_info['coi_class'])
        
        # Show the edit form
        self.edit_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Disable the ID field for existing companies
        self.id_entry.config(state="disabled")
        
        # Show the data objects
        self.show_data_objects(company_id)
    
    def show_data_objects(self, company_id):
        """Show the company's data objects"""
        # Clear the current objects list
        for item in self.objects_tree.get_children():
            self.objects_tree.delete(item)
        
        # Get the company's objects
        company_objects = self.model.get_company_objects(company_id)
        
        # Add all objects to the list
        for object_id, object_data in company_objects.items():
            self.objects_tree.insert('', tk.END, values=(object_id, object_data))
        
        # Show the objects frame and content
        self.objects_content.pack(fill=tk.BOTH, expand=True)
        self.objects_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def on_object_select(self, event):
        """Handle object selection in the treeview"""
        # This is used for the context menu
        pass
    
    def add_company(self):
        """Add a new company"""
        # Hide the select label
        self.select_label.pack_forget()
        
        # Clear the company details
        self.company_id_var.set("")
        self.company_name_var.set("")
        if self.model.coi_classes:
            self.company_coi_var.set(list(self.model.coi_classes.keys())[0])
        else:
            self.company_coi_var.set("")
        
        # Enable the ID field for new companies
        self.id_entry.config(state="normal")
        
        # Show the edit form
        self.edit_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Hide the objects frame
        self.objects_frame.pack_forget()
    
    def save_company(self):
        """Save the company details"""
        # Get the company details
        company_id = self.company_id_var.get()
        company_name = self.company_name_var.get()
        company_coi = self.company_coi_var.get()
        
        # Validate the input
        if not company_id or not company_name or not company_coi:
            messagebox.showerror("Error", "All fields are required")
            return
        
        # Check if this is a new company or an update
        if company_id in self.model.companies:
            # Update existing company
            old_coi = self.model.companies[company_id]['coi_class']
            
            # If COI class changed, we need to move the company
            if old_coi != company_coi:
                # Remove from old COI class
                if company_id in self.model.coi_classes[old_coi]:
                    company_objects = self.model.coi_classes[old_coi][company_id]
                    del self.model.coi_classes[old_coi][company_id]
                    
                    # Add to new COI class
                    if company_id not in self.model.coi_classes[company_coi]:
                        self.model.coi_classes[company_coi][company_id] = company_objects
            
            # Update company info
            self.model.companies[company_id]['name'] = company_name
            self.model.companies[company_id]['coi_class'] = company_coi
            
            messagebox.showinfo("Success", f"Company '{company_name}' updated successfully")
        else:
            # Add new company
            success = self.data_manager.add_new_company(company_id, company_name, company_coi)
            if success:
                messagebox.showinfo("Success", f"Company '{company_name}' added successfully")
            else:
                messagebox.showerror("Error", f"Failed to add company '{company_name}'")
        
        # Refresh the company list
        self.refresh_company_list()
        
        # Reset the form
        self.cancel_edit()
    
    def delete_company(self):
        """Delete the selected company"""
        company_id = self.company_id_var.get()
        company_name = self.company_name_var.get()
        
        if not company_id or company_id not in self.model.companies:
            messagebox.showerror("Error", "No valid company selected")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", 
                                  f"Are you sure you want to delete company '{company_name}'?"):
            return
        
        # Get the COI class
        coi_class = self.model.companies[company_id]['coi_class']
        
        # Delete the company from the COI class
        if company_id in self.model.coi_classes[coi_class]:
            del self.model.coi_classes[coi_class][company_id]
        
        # Delete the company from the companies dict
        del self.model.companies[company_id]
        
        # Delete the company from all user access histories
        for user_id in self.model.user_access_history:
            if company_id in self.model.user_access_history[user_id]:
                del self.model.user_access_history[user_id][company_id]
        
        messagebox.showinfo("Success", f"Company '{company_name}' deleted successfully")
        
        # Refresh the company list
        self.refresh_company_list()
        
        # Reset the form
        self.cancel_edit()
    
    def cancel_edit(self):
        """Cancel editing and reset the form"""
        # Hide the edit form
        self.edit_frame.pack_forget()
        
        # Hide the objects frame
        self.objects_frame.pack_forget()
        
        # Show the select label
        self.select_label.pack(padx=20, pady=20)
        
        # Clear the selection in the treeview
        self.company_tree.selection_remove(self.company_tree.selection())
    
    def add_data_object(self):
        """Add a new data object to the selected company"""
        company_id = self.company_id_var.get()
        
        if not company_id or company_id not in self.model.companies:
            messagebox.showerror("Error", "No valid company selected")
            return
        
        # Ask for object ID
        object_id = simpledialog.askstring("Add Data Object", "Enter Object ID:")
        if not object_id:
            return
        
        # Ask for object data
        object_data = simpledialog.askstring("Add Data Object", "Enter Object Data:")
        if not object_data:
            return
        
        # Add the object
        success = self.data_manager.add_new_object(company_id, object_id, object_data)
        
        if success:
            messagebox.showinfo("Success", f"Data object '{object_id}' added successfully")
            # Refresh the objects list
            self.show_data_objects(company_id)
        else:
            messagebox.showerror("Error", f"Failed to add data object '{object_id}'")
    
    def edit_data_object(self):
        """Edit the selected data object"""
        company_id = self.company_id_var.get()
        
        if not company_id or company_id not in self.model.companies:
            messagebox.showerror("Error", "No valid company selected")
            return
        
        # Get the selected object
        selected_items = self.objects_tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "No data object selected")
            return
        
        # Get the object ID from the selected item
        item = selected_items[0]
        object_id = self.objects_tree.item(item, 'values')[0]
        
        # Get the current data
        company_objects = self.model.get_company_objects(company_id)
        if object_id not in company_objects:
            messagebox.showerror("Error", f"Data object '{object_id}' not found")
            return
        
        current_data = company_objects[object_id]
        
        # Ask for new data
        new_data = simpledialog.askstring("Edit Data Object", 
                                         "Enter new data:", 
                                         initialvalue=current_data)
        if new_data is None:  # User cancelled
            return
        
        # Update the object
        coi_class = self.model.companies[company_id]['coi_class']
        self.model.coi_classes[coi_class][company_id][object_id] = new_data
        
        messagebox.showinfo("Success", f"Data object '{object_id}' updated successfully")
        
        # Refresh the objects list
        self.show_data_objects(company_id)
    
    def delete_data_object(self):
        """Delete the selected data object"""
        company_id = self.company_id_var.get()
        
        if not company_id or company_id not in self.model.companies:
            messagebox.showerror("Error", "No valid company selected")
            return
        
        # Get the selected object
        selected_items = self.objects_tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "No data object selected")
            return
        
        # Get the object ID from the selected item
        item = selected_items[0]
        object_id = self.objects_tree.item(item, 'values')[0]
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", 
                                  f"Are you sure you want to delete data object '{object_id}'?"):
            return
        
        # Delete the object
        coi_class = self.model.companies[company_id]['coi_class']
        if object_id in self.model.coi_classes[coi_class][company_id]:
            del self.model.coi_classes[coi_class][company_id][object_id]
            
            messagebox.showinfo("Success", f"Data object '{object_id}' deleted successfully")
            
            # Refresh the objects list
            self.show_data_objects(company_id)
        else:
            messagebox.showerror("Error", f"Data object '{object_id}' not found")
