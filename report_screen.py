"""
Report Screen for Chinese Wall Model Demonstration
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib
matplotlib.use('TkAgg')  # Set the backend for matplotlib
from utils import create_tooltip, create_scrollable_frame

class ReportScreen(ttk.Frame):
    def __init__(self, parent, model, report_generator, current_user, back_callback):
        super().__init__(parent)
        self.parent = parent
        self.model = model
        self.report_generator = report_generator
        self.current_user = current_user
        self.back_callback = back_callback
        
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
    
    def create_widgets(self):
        """Create the widgets for the report screen"""
        # Header with back button
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        back_button = ttk.Button(header_frame, text="← Back to Dashboard", 
                                command=self.back_callback)
        back_button.pack(side=tk.LEFT)
        
        title_label = ttk.Label(header_frame, text="Access Reports & Analytics", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(side=tk.LEFT, padx=20)
        
        # Main content
        content_frame = ttk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook for different report types
        notebook = ttk.Notebook(content_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Access Log tab
        access_log_tab = ttk.Frame(notebook)
        notebook.add(access_log_tab, text="Access Log")
        self.create_access_log_tab(access_log_tab)
        
        # Analytics tab
        analytics_tab = ttk.Frame(notebook)
        notebook.add(analytics_tab, text="Analytics")
        self.create_analytics_tab(analytics_tab)
        
        # Structure Visualization tab
        structure_tab = ttk.Frame(notebook)
        notebook.add(structure_tab, text="COI Structure")
        self.create_structure_tab(structure_tab)
        
        # Export Reports tab
        export_tab = ttk.Frame(notebook)
        notebook.add(export_tab, text="Export Reports")
        self.create_export_tab(export_tab)
    
    def create_access_log_tab(self, parent):
        """Create the Access Log tab"""
        # Controls frame
        controls_frame = ttk.Frame(parent)
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Filter options
        ttk.Label(controls_frame, text="Filter by:").pack(side=tk.LEFT, padx=5)
        
        # User filter
        self.user_filter_var = tk.StringVar(value="All Users")
        user_filter = ttk.Combobox(controls_frame, textvariable=self.user_filter_var, 
                                  state="readonly", width=15)
        user_options = ["All Users"] + [f"{info['name']}" for uid, info in self.model.users.items()]
        user_filter['values'] = user_options
        user_filter.pack(side=tk.LEFT, padx=5)
        
        # Company filter
        self.company_filter_var = tk.StringVar(value="All Companies")
        company_filter = ttk.Combobox(controls_frame, textvariable=self.company_filter_var, 
                                     state="readonly", width=15)
        company_options = ["All Companies"] + [f"{info['name']}" for cid, info in self.model.companies.items()]
        company_filter['values'] = company_options
        company_filter.pack(side=tk.LEFT, padx=5)
        
        # Access status filter
        self.status_filter_var = tk.StringVar(value="All")
        status_filter = ttk.Combobox(controls_frame, textvariable=self.status_filter_var, 
                                    state="readonly", width=15)
        status_filter['values'] = ["All", "Granted", "Denied"]
        status_filter.pack(side=tk.LEFT, padx=5)
        
        # Apply filter button
        apply_button = ttk.Button(controls_frame, text="Apply Filters", 
                                 command=self.update_access_log)
        apply_button.pack(side=tk.LEFT, padx=10)
        
        # Log frame
        log_frame = ttk.LabelFrame(parent, text="Access Log Entries")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create scrollable text widget for logs
        self.log_text = tk.Text(log_frame, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add scrollbar to log text
        log_scrollbar = ttk.Scrollbar(self.log_text, command=self.log_text.yview)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=log_scrollbar.set)
        
        # Disable text editing
        self.log_text.config(state=tk.DISABLED)
        
        # Initial update
        self.update_access_log()
    
    def create_analytics_tab(self, parent):
        """Create the Analytics tab"""
        # Create frame for charts
        charts_frame = ttk.Frame(parent)
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Summary chart
        summary_frame = ttk.LabelFrame(charts_frame, text="Access Attempts Summary")
        summary_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create and add the chart
        summary_chart = self.report_generator.create_access_summary_chart(summary_frame)
        summary_chart.pack(fill=tk.BOTH, expand=True)
        
        # Company access chart
        company_frame = ttk.LabelFrame(charts_frame, text="Access by Company")
        company_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create and add the chart
        company_chart = self.report_generator.create_company_access_chart(company_frame)
        company_chart.pack(fill=tk.BOTH, expand=True)
        
        # User access chart
        user_frame = ttk.LabelFrame(charts_frame, text="Access by User")
        user_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create and add the chart
        user_chart = self.report_generator.create_user_access_chart(user_frame)
        user_chart.pack(fill=tk.BOTH, expand=True)
    
    def create_structure_tab(self, parent):
        """Create the Structure Visualization tab"""
        # Create frame for visualization
        viz_frame = ttk.Frame(parent)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add explanation
        explanation_frame = ttk.LabelFrame(viz_frame, text="Chinese Wall Structure")
        explanation_frame.pack(fill=tk.X, padx=10, pady=10)
        
        explanation_text = """
This visualization shows the structure of the Chinese Wall Model:

- Each rectangle represents a Conflict of Interest (COI) Class
- Companies within the same COI Class are in competition with each other
- Once a user accesses data from one company in a COI Class, they cannot access data from any other company in the same class
- Companies in different COI Classes are not in conflict with each other
        """
        
        explanation_label = ttk.Label(explanation_frame, text=explanation_text, 
                                     justify=tk.LEFT, wraplength=600)
        explanation_label.pack(padx=10, pady=10)
        
        # Create visualization
        structure_frame = ttk.LabelFrame(viz_frame, text="Visualization")
        structure_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create and add the visualization
        structure_viz = self.report_generator.visualize_coi_structure(structure_frame)
        structure_viz.pack(fill=tk.BOTH, expand=True)
    
    def create_export_tab(self, parent):
        """Create the Export Reports tab"""
        # Create frame for export options
        export_frame = ttk.Frame(parent)
        export_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Export options
        options_frame = ttk.LabelFrame(export_frame, text="Export Options")
        options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Report type
        ttk.Label(options_frame, text="Report Type:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        
        self.report_type_var = tk.StringVar(value="Complete Access Log")
        report_type = ttk.Combobox(options_frame, textvariable=self.report_type_var, 
                                  state="readonly", width=30)
        report_type['values'] = [
            "Complete Access Log", 
            "User-Specific Report", 
            "Company-Specific Report"
        ]
        report_type.grid(row=0, column=1, padx=10, pady=10)
        
        # User selection for user-specific report
        ttk.Label(options_frame, text="User:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        
        self.user_var = tk.StringVar()
        user_combobox = ttk.Combobox(options_frame, textvariable=self.user_var, 
                                    state="readonly", width=30)
        user_options = [(uid, f"{info['name']}") for uid, info in self.model.users.items()]
        user_combobox['values'] = [option[1] for option in user_options]
        user_combobox.grid(row=1, column=1, padx=10, pady=10)
        
        # Store the mapping of display names to user IDs
        self.user_id_map = {option[1]: option[0] for option in user_options}
        
        # Company selection for company-specific report
        ttk.Label(options_frame, text="Company:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        
        self.company_var = tk.StringVar()
        company_combobox = ttk.Combobox(options_frame, textvariable=self.company_var, 
                                       state="readonly", width=30)
        company_options = [(cid, f"{info['name']}") for cid, info in self.model.companies.items()]
        company_combobox['values'] = [option[1] for option in company_options]
        company_combobox.grid(row=2, column=1, padx=10, pady=10)
        
        # Store the mapping of display names to company IDs
        self.company_id_map = {option[1]: option[0] for option in company_options}
        
        # Format selection
        ttk.Label(options_frame, text="Format:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        
        self.format_var = tk.StringVar(value="Text")
        format_combobox = ttk.Combobox(options_frame, textvariable=self.format_var, 
                                      state="readonly", width=30)
        format_combobox['values'] = ["Text", "CSV"]
        format_combobox.grid(row=3, column=1, padx=10, pady=10)
        
        # Export button
        export_button = ttk.Button(options_frame, text="Export Report", 
                                  command=self.export_report)
        export_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20)
        
        # Preview frame
        preview_frame = ttk.LabelFrame(export_frame, text="Report Preview")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create scrollable text widget for preview
        self.preview_text = tk.Text(preview_frame, wrap=tk.WORD)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add scrollbar to preview text
        preview_scrollbar = ttk.Scrollbar(self.preview_text, command=self.preview_text.yview)
        preview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.preview_text.config(yscrollcommand=preview_scrollbar.set)
        
        # Disable text editing
        self.preview_text.config(state=tk.DISABLED)
        
        # Add button to update preview
        preview_button = ttk.Button(options_frame, text="Update Preview", 
                                   command=self.update_preview)
        preview_button.grid(row=4, column=2, padx=10, pady=20)
    
    def update_access_log(self):
        """Update the access log based on filters"""
        logs = self.model.access_logs
        
        # Apply filters
        if self.user_filter_var.get() != "All Users":
            user_name = self.user_filter_var.get()
            logs = [log for log in logs if log['user_name'] == user_name]
        
        if self.company_filter_var.get() != "All Companies":
            company_name = self.company_filter_var.get()
            logs = [log for log in logs if log['company_name'] == company_name]
        
        if self.status_filter_var.get() != "All":
            status = self.status_filter_var.get() == "Granted"
            logs = [log for log in logs if log['access_granted'] == status]
        
        # Update the log text
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        
        for log in logs:
            status = "GRANTED" if log['access_granted'] else "DENIED"
            color = "green" if log['access_granted'] else "red"
            
            self.log_text.insert(tk.END, f"[{log['timestamp']}] ")
            self.log_text.insert(tk.END, f"{log['user_name']} -> {log['company_name']} ({log['object_id']}): ")
            self.log_text.insert(tk.END, f"{status}\n", (status.lower(),))
            self.log_text.insert(tk.END, f"  Reason: {log['reason']}\n\n")
            
            # Configure tags for coloring
            self.log_text.tag_configure("granted", foreground="green")
            self.log_text.tag_configure("denied", foreground="red")
        
        self.log_text.config(state=tk.DISABLED)
    
    def update_preview(self):
        """Update the report preview"""
        report_type = self.report_type_var.get()
        
        # Generate appropriate report
        if report_type == "Complete Access Log":
            report = self.report_generator.generate_access_report(output_format="text")
        
        elif report_type == "User-Specific Report":
            user_name = self.user_var.get()
            if not user_name:
                messagebox.showwarning("Warning", "Please select a user")
                return
            
            user_id = self.user_id_map[user_name]
            report = self.report_generator.generate_user_report(user_id)
        
        elif report_type == "Company-Specific Report":
            company_name = self.company_var.get()
            if not company_name:
                messagebox.showwarning("Warning", "Please select a company")
                return
            
            company_id = self.company_id_map[company_name]
            report = self.report_generator.generate_company_report(company_id)
        
        # Update the preview
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, report)
        self.preview_text.config(state=tk.DISABLED)
    
    def export_report(self):
        """Export the report to a file"""
        report_type = self.report_type_var.get()
        format_type = self.format_var.get()
        
        # Determine file extension
        extension = ".txt" if format_type == "Text" else ".csv"
        
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=extension,
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")],
            title="Save Report As"
        )
        
        if not file_path:
            return  # User cancelled
        
        try:
            if format_type == "Text":
                # Generate appropriate text report
                if report_type == "Complete Access Log":
                    report = self.report_generator.generate_access_report(output_format="text")
                
                elif report_type == "User-Specific Report":
                    user_name = self.user_var.get()
                    if not user_name:
                        messagebox.showwarning("Warning", "Please select a user")
                        return
                    
                    user_id = self.user_id_map[user_name]
                    report = self.report_generator.generate_user_report(user_id)
                
                elif report_type == "Company-Specific Report":
                    company_name = self.company_var.get()
                    if not company_name:
                        messagebox.showwarning("Warning", "Please select a company")
                        return
                    
                    company_id = self.company_id_map[company_name]
                    report = self.report_generator.generate_company_report(company_id)
                
                # Write to file
                with open(file_path, 'w') as f:
                    f.write(report)
            
            else:  # CSV format
                # For CSV, we always use the full log but may filter it
                logs = self.model.access_logs
                
                # Apply filters based on report type
                if report_type == "User-Specific Report":
                    user_name = self.user_var.get()
                    if not user_name:
                        messagebox.showwarning("Warning", "Please select a user")
                        return
                    
                    user_id = self.user_id_map[user_name]
                    logs = [log for log in logs if log['user_id'] == user_id]
                
                elif report_type == "Company-Specific Report":
                    company_name = self.company_var.get()
                    if not company_name:
                        messagebox.showwarning("Warning", "Please select a company")
                        return
                    
                    company_id = self.company_id_map[company_name]
                    logs = [log for log in logs if log['company_id'] == company_id]
                
                # Write to CSV
                import csv
                with open(file_path, 'w', newline='') as csvfile:
                    fieldnames = ['timestamp', 'user_name', 'company_name', 'object_id', 
                                 'access_granted', 'reason']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for log in logs:
                        writer.writerow({
                            'timestamp': log['timestamp'],
                            'user_name': log['user_name'],
                            'company_name': log['company_name'],
                            'object_id': log['object_id'],
                            'access_granted': log['access_granted'],
                            'reason': log['reason']
                        })
            
            messagebox.showinfo("Export Complete", f"Report exported successfully to {file_path}")
        
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting report: {str(e)}")
