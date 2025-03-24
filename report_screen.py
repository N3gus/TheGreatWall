"""
Report Screen for Chinese Wall Model Demonstration
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib
matplotlib.use('TkAgg')  # Set the backend for matplotlib
from utils import (create_tooltip, create_scrollable_frame, create_section_header, 
                  create_card, create_badge, create_notification, create_data_table,
                  create_info_box)
import datetime

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
        create_tooltip(back_button, "Return to the main dashboard")
        
        title_label = ttk.Label(header_frame, text="Access Reports & Analytics", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(side=tk.LEFT, padx=20)
        
        # User info badge
        user_info = self.model.users[self.current_user]
        user_frame = tk.Frame(header_frame, bg="#f0f0f0", padx=5, pady=2)
        user_frame.pack(side=tk.RIGHT)
        
        user_label = tk.Label(user_frame, text=f"Viewing as: {user_info['name']}", 
                             bg="#f0f0f0", font=('Arial', 9))
        user_label.pack(side=tk.LEFT, padx=(0, 5))
        
        role_badge = create_badge(user_frame, user_info['role'].capitalize())
        role_badge.pack(side=tk.LEFT)
        
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
        controls_card = create_card(parent, "Filter Options", title_bg="#e3f2fd")
        
        # Controls content
        controls_content = tk.Frame(controls_card, bg="white")
        controls_content.pack(fill=tk.X, padx=15, pady=15)
        
        # Filter options with improved layout
        filters_frame = tk.Frame(controls_content, bg="white")
        filters_frame.pack(fill=tk.X)
        
        # User filter
        user_filter_frame = tk.Frame(filters_frame, bg="white")
        user_filter_frame.pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(user_filter_frame, text="User:", bg="white", 
                font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        self.user_filter_var = tk.StringVar(value="All Users")
        user_filter = ttk.Combobox(user_filter_frame, textvariable=self.user_filter_var, 
                                  state="readonly", width=15)
        user_options = ["All Users"] + [f"{info['name']}" for uid, info in self.model.users.items()]
        user_filter['values'] = user_options
        user_filter.pack(pady=2)
        
        # Company filter
        company_filter_frame = tk.Frame(filters_frame, bg="white")
        company_filter_frame.pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(company_filter_frame, text="Company:", bg="white", 
                font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        self.company_filter_var = tk.StringVar(value="All Companies")
        company_filter = ttk.Combobox(company_filter_frame, textvariable=self.company_filter_var, 
                                     state="readonly", width=15)
        company_options = ["All Companies"] + [f"{info['name']}" for cid, info in self.model.companies.items()]
        company_filter['values'] = company_options
        company_filter.pack(pady=2)
        
        # Access status filter
        status_filter_frame = tk.Frame(filters_frame, bg="white")
        status_filter_frame.pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(status_filter_frame, text="Status:", bg="white", 
                font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        self.status_filter_var = tk.StringVar(value="All")
        status_filter = ttk.Combobox(status_filter_frame, textvariable=self.status_filter_var, 
                                    state="readonly", width=15)
        status_filter['values'] = ["All", "Granted", "Denied"]
        status_filter.pack(pady=2)
        
        # Date filter
        date_filter_frame = tk.Frame(filters_frame, bg="white")
        date_filter_frame.pack(side=tk.LEFT)
        
        tk.Label(date_filter_frame, text="Date Range:", bg="white", 
                font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        date_options_frame = tk.Frame(date_filter_frame, bg="white")
        date_options_frame.pack(fill=tk.X)
        
        self.date_filter_var = tk.StringVar(value="All Time")
        date_filter = ttk.Combobox(date_options_frame, textvariable=self.date_filter_var, 
                                  state="readonly", width=15)
        date_filter['values'] = ["All Time", "Today", "Last 7 Days", "Last 30 Days"]
        date_filter.pack(side=tk.LEFT, pady=2)
        
        # Apply filter button
        button_frame = tk.Frame(controls_content, bg="white")
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        apply_button = ttk.Button(button_frame, text="Apply Filters", 
                                 command=self.update_access_log)
        apply_button.pack(side=tk.RIGHT)
        create_tooltip(apply_button, "Apply the selected filters to the access log")
        
        clear_button = ttk.Button(button_frame, text="Clear Filters", 
                                 command=self.clear_filters)
        clear_button.pack(side=tk.RIGHT, padx=5)
        create_tooltip(clear_button, "Reset all filters to their default values")
        
        # Log frame
        log_card = create_card(parent, "Access Log Entries", title_bg="#e3f2fd")
        
        # Create table for access log
        table_frame = tk.Frame(log_card, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Create the table headers
        headers = ["Timestamp", "User", "Company", "Object", "Status", "Reason"]
        
        # Get the log data
        self.log_data = self.get_filtered_log_data()
        
        # Create the table
        self.log_table = create_data_table(table_frame, headers, self.log_data)
        
        # Status message
        self.status_label = tk.Label(log_card, text=f"Showing {len(self.log_data)} entries", 
                                    bg="white", fg="#757575", font=('Arial', 9))
        self.status_label.pack(side=tk.RIGHT, padx=15, pady=(0, 10))
    
    def create_analytics_tab(self, parent):
        """Create the Analytics tab"""
        # Create scrollable frame for charts
        scrollable_frame = create_scrollable_frame(parent)
        
        # Summary section
        summary_section = create_section_header(scrollable_frame, "Access Attempts Summary")
        
        # Summary info box
        summary_stats = self.report_generator.get_summary_statistics()
        summary_text = (
            f"Total Access Attempts: {summary_stats['total']}\n"
            f"Granted: {summary_stats['granted']} ({summary_stats['granted_percent']}%)\n"
            f"Denied: {summary_stats['denied']} ({summary_stats['denied_percent']}%)"
        )
        
        create_info_box(scrollable_frame, "Summary Statistics", summary_text, 
                       bg_color="#e8f5e9", border_color="#4caf50")
        
        # Summary chart card
        summary_card = create_card(scrollable_frame, "Access Attempts Chart")
        
        # Create and add the chart
        summary_chart_frame = tk.Frame(summary_card, bg="white")
        summary_chart_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        summary_chart = self.report_generator.create_access_summary_chart(summary_chart_frame)
        summary_chart.pack(fill=tk.BOTH, expand=True)
        
        # Company section
        company_section = create_section_header(scrollable_frame, "Access by Company")
        
        # Company access chart card
        company_card = create_card(scrollable_frame, "Company Access Distribution")
        
        # Create and add the chart
        company_chart_frame = tk.Frame(company_card, bg="white")
        company_chart_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        company_chart = self.report_generator.create_company_access_chart(company_chart_frame)
        company_chart.pack(fill=tk.BOTH, expand=True)
        
        # User section
        user_section = create_section_header(scrollable_frame, "Access by User")
        
        # User access chart card
        user_card = create_card(scrollable_frame, "User Activity")
        
        # Create and add the chart
        user_chart_frame = tk.Frame(user_card, bg="white")
        user_chart_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        user_chart = self.report_generator.create_user_access_chart(user_chart_frame)
        user_chart.pack(fill=tk.BOTH, expand=True)
    
    def create_structure_tab(self, parent):
        """Create the Structure Visualization tab"""
        # Create scrollable frame for visualization
        scrollable_frame = create_scrollable_frame(parent)
        
        # Explanation section
        explanation_section = create_section_header(scrollable_frame, "Chinese Wall Structure")
        
        # Add explanation in an info box
        explanation_text = """
The Chinese Wall Model organizes companies into Conflict of Interest (COI) Classes.

Key principles:
• Companies within the same COI Class are in competition with each other
• Once a user accesses data from one company in a COI Class, they cannot access data from any other company in the same class
• Companies in different COI Classes are not in conflict with each other

This visualization shows the structure of COI Classes and the companies within them.
        """
        
        create_info_box(scrollable_frame, "Understanding the Visualization", explanation_text, 
                       bg_color="#e3f2fd", border_color="#1976d2")
        
        # Create visualization card
        structure_card = create_card(scrollable_frame, "COI Structure Visualization")
        
        # Create and add the visualization
        structure_frame = tk.Frame(structure_card, bg="white")
        structure_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        structure_viz = self.report_generator.visualize_coi_structure(structure_frame)
        structure_viz.pack(fill=tk.BOTH, expand=True)
        
        # Add legend
        legend_frame = tk.Frame(scrollable_frame, bg="white")
        legend_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Create a card for the legend
        legend_card = create_card(scrollable_frame, "Legend")
        
        # Legend content
        legend_content = tk.Frame(legend_card, bg="white")
        legend_content.pack(fill=tk.X, padx=15, pady=15)
        
        # COI Class
        coi_frame = tk.Frame(legend_content, bg="white")
        coi_frame.pack(fill=tk.X, pady=2)
        
        coi_color = tk.Frame(coi_frame, bg="#1976d2", width=20, height=20)
        coi_color.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(coi_frame, text="COI Class", bg="white", 
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        # Company
        company_frame = tk.Frame(legend_content, bg="white")
        company_frame.pack(fill=tk.X, pady=2)
        
        company_color = tk.Frame(company_frame, bg="#4caf50", width=20, height=20)
        company_color.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(company_frame, text="Company", bg="white", 
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        # User's accessed company
        accessed_frame = tk.Frame(legend_content, bg="white")
        accessed_frame.pack(fill=tk.X, pady=2)
        
        accessed_color = tk.Frame(accessed_frame, bg="#ff9800", width=20, height=20)
        accessed_color.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(accessed_frame, text="Company Accessed by Current User", bg="white", 
                font=('Arial', 10)).pack(side=tk.LEFT)
    
    def create_export_tab(self, parent):
        """Create the Export Reports tab"""
        # Create scrollable frame for export options
        scrollable_frame = create_scrollable_frame(parent)
        
        # Export options section
        options_section = create_section_header(scrollable_frame, "Export Options")
        
        # Export options card
        options_card = create_card(scrollable_frame, "Configure Report")
        
        # Options content
        options_content = tk.Frame(options_card, bg="white")
        options_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Report type
        type_frame = tk.Frame(options_content, bg="white")
        type_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(type_frame, text="Report Type:", bg="white", 
                font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        self.report_type_var = tk.StringVar(value="Complete Access Log")
        report_type = ttk.Combobox(type_frame, textvariable=self.report_type_var, 
                                  state="readonly", width=30)
        report_type['values'] = [
            "Complete Access Log", 
            "User-Specific Report", 
            "Company-Specific Report",
            "COI Class Analysis",
            "Security Audit Report"
        ]
        report_type.pack(anchor=tk.W, pady=2)
        
        # Format options
        format_frame = tk.Frame(options_content, bg="white")
        format_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(format_frame, text="Export Format:", bg="white", 
                font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        self.format_var = tk.StringVar(value="CSV")
        
        format_options_frame = tk.Frame(format_frame, bg="white")
        format_options_frame.pack(anchor=tk.W)
        
        formats = [("CSV", "CSV"), ("Text", "TXT"), ("PDF", "PDF")]
        for text, value in formats:
            ttk.Radiobutton(format_options_frame, text=text, value=value, 
                           variable=self.format_var).pack(side=tk.LEFT, padx=10)
        
        # Include charts option
        charts_frame = tk.Frame(options_content, bg="white")
        charts_frame.pack(fill=tk.X, pady=5)
        
        self.include_charts_var = tk.BooleanVar(value=True)
        charts_check = ttk.Checkbutton(charts_frame, text="Include charts and visualizations", 
                                      variable=self.include_charts_var)
        charts_check.pack(anchor=tk.W)
        
        # Date range
        date_frame = tk.Frame(options_content, bg="white")
        date_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(date_frame, text="Date Range:", bg="white", 
                font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        date_options_frame = tk.Frame(date_frame, bg="white")
        date_options_frame.pack(anchor=tk.W)
        
        self.date_range_var = tk.StringVar(value="All Time")
        date_options = ttk.Combobox(date_options_frame, textvariable=self.date_range_var, 
                                   state="readonly", width=15)
        date_options['values'] = ["All Time", "Today", "Last 7 Days", "Last 30 Days", "Custom Range"]
        date_options.pack(side=tk.LEFT, pady=2)
        
        # Export button
        button_frame = tk.Frame(options_content, bg="white")
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        export_button = ttk.Button(button_frame, text="Export Report", 
                                  command=self.export_report,
                                  style="Accent.TButton")
        export_button.pack(side=tk.RIGHT)
        create_tooltip(export_button, "Generate and save the report with the selected options")
        
        # Preview section
        preview_section = create_section_header(scrollable_frame, "Report Preview")
        
        # Preview card
        preview_card = create_card(scrollable_frame, "Preview")
        
        # Preview content
        preview_content = tk.Frame(preview_card, bg="white")
        preview_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Preview text
        self.preview_text = tk.Text(preview_content, wrap=tk.WORD, height=15, 
                                   font=('Courier', 10), bg='#f8f9fa', bd=1)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add scrollbar to preview text
        preview_scrollbar = ttk.Scrollbar(self.preview_text, command=self.preview_text.yview)
        preview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.preview_text.config(yscrollcommand=preview_scrollbar.set)
        
        # Disable text editing
        self.preview_text.config(state=tk.DISABLED)
        
        # Generate preview button
        preview_button = ttk.Button(preview_content, text="Generate Preview", 
                                   command=self.update_preview)
        preview_button.pack(side=tk.RIGHT, pady=(5, 0))
        create_tooltip(preview_button, "Generate a preview of the report with current settings")
    
    def update_access_log(self):
        """Update the access log based on the selected filters"""
        # Get filtered log data
        self.log_data = self.get_filtered_log_data()
        
        # Clear existing table
        for item in self.log_table.get_children():
            self.log_table.delete(item)
        
        # Insert new data
        for row in self.log_data:
            self.log_table.insert('', 'end', values=row)
        
        # Update status label
        self.status_label.config(text=f"Showing {len(self.log_data)} entries")
        
        # Show notification
        create_notification(self, f"Access log updated with {len(self.log_data)} entries", "info")
    
    def clear_filters(self):
        """Reset all filters to their default values"""
        self.user_filter_var.set("All Users")
        self.company_filter_var.set("All Companies")
        self.status_filter_var.set("All")
        self.date_filter_var.set("All Time")
        
        # Update the log
        self.update_access_log()
    
    def get_filtered_log_data(self):
        """Get access log data based on the selected filters"""
        # Get all access log entries
        all_logs = self.report_generator.get_access_log()
        
        # Apply filters
        filtered_logs = []
        for log in all_logs:
            # Check user filter
            if self.user_filter_var.get() != "All Users" and log['user_name'] != self.user_filter_var.get():
                continue
            
            # Check company filter
            if self.company_filter_var.get() != "All Companies" and log['company_name'] != self.company_filter_var.get():
                continue
            
            # Check status filter
            if self.status_filter_var.get() == "Granted" and not log['granted']:
                continue
            if self.status_filter_var.get() == "Denied" and log['granted']:
                continue
            
            # Check date filter
            if self.date_filter_var.get() != "All Time":
                log_date = datetime.datetime.strptime(log['timestamp'], "%Y-%m-%d %H:%M:%S")
                now = datetime.datetime.now()
                
                if self.date_filter_var.get() == "Today":
                    if log_date.date() != now.date():
                        continue
                elif self.date_filter_var.get() == "Last 7 Days":
                    if (now - log_date).days > 7:
                        continue
                elif self.date_filter_var.get() == "Last 30 Days":
                    if (now - log_date).days > 30:
                        continue
            
            # Format the row for the table
            status_text = "Granted" if log['granted'] else "Denied"
            row = [
                log['timestamp'],
                log['user_name'],
                log['company_name'],
                log['object_id'],
                status_text,
                log['reason']
            ]
            filtered_logs.append(row)
        
        # Sort by timestamp (newest first)
        filtered_logs.sort(key=lambda x: x[0], reverse=True)
        
        return filtered_logs
    
    def update_preview(self):
        """Update the report preview"""
        # Get the report content
        report_content = self.report_generator.generate_report_preview(
            report_type=self.report_type_var.get(),
            date_range=self.date_range_var.get(),
            include_charts=self.include_charts_var.get()
        )
        
        # Update the preview text
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, report_content)
        self.preview_text.config(state=tk.DISABLED)
        
        # Show notification
        create_notification(self, "Report preview generated", "info")
    
    def export_report(self):
        """Export the report with the selected options"""
        # Get the file extension
        file_ext = self.format_var.get().lower()
        
        # Create default filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"chinese_wall_report_{timestamp}.{file_ext}"
        
        # Ask for save location
        filepath = filedialog.asksaveasfilename(
            defaultextension=f".{file_ext}",
            filetypes=[(f"{self.format_var.get()} files", f"*.{file_ext}")],
            initialfile=default_filename
        )
        
        if not filepath:
            return  # User cancelled
        
        try:
            # Generate and save the report
            self.report_generator.export_report(
                filepath=filepath,
                report_type=self.report_type_var.get(),
                format_type=self.format_var.get(),
                date_range=self.date_range_var.get(),
                include_charts=self.include_charts_var.get()
            )
            
            # Show success notification
            create_notification(self, f"Report exported successfully to {filepath}", "success")
            
        except Exception as e:
            # Show error notification
            create_notification(self, f"Error exporting report: {str(e)}", "error")
