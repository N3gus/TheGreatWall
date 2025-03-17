"""
Report Generator for Chinese Wall Model Application
Handles generation of reports and visualizations
"""

import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ReportGenerator:
    def __init__(self, model):
        """Initialize with a reference to the ChineseWallModel instance"""
        self.model = model
    
    def generate_access_report(self, output_format="dict"):
        """
        Generate a report of all access attempts
        output_format: 'dict', 'csv', or 'text'
        """
        logs = self.model.access_logs
        
        if output_format == "dict":
            return logs
        
        elif output_format == "csv":
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"access_report_{timestamp}.csv"
            
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['timestamp', 'user_name', 'company_name', 'object_id', 'access_granted', 'reason']
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
            
            return filename
        
        elif output_format == "text":
            report = "ACCESS REPORT\n"
            report += "=" * 80 + "\n"
            report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            report += "=" * 80 + "\n\n"
            
            for log in logs:
                status = "GRANTED" if log['access_granted'] else "DENIED"
                report += f"[{log['timestamp']}] {log['user_name']} -> {log['company_name']} ({log['object_id']}): {status}\n"
                report += f"  Reason: {log['reason']}\n\n"
            
            return report
    
    def generate_user_report(self, user_id):
        """Generate a report for a specific user's access history"""
        logs = [log for log in self.model.access_logs if log['user_id'] == user_id]
        
        report = f"ACCESS REPORT FOR USER: {self.model.users[user_id]['name']}\n"
        report += "=" * 80 + "\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "=" * 80 + "\n\n"
        
        for log in logs:
            status = "GRANTED" if log['access_granted'] else "DENIED"
            report += f"[{log['timestamp']}] {log['company_name']} ({log['object_id']}): {status}\n"
            report += f"  Reason: {log['reason']}\n\n"
        
        return report
    
    def generate_company_report(self, company_id):
        """Generate a report for a specific company's access attempts"""
        logs = [log for log in self.model.access_logs if log['company_id'] == company_id]
        
        report = f"ACCESS REPORT FOR COMPANY: {self.model.companies[company_id]['name']}\n"
        report += "=" * 80 + "\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "=" * 80 + "\n\n"
        
        for log in logs:
            status = "GRANTED" if log['access_granted'] else "DENIED"
            report += f"[{log['timestamp']}] User: {log['user_name']} - Object: {log['object_id']}: {status}\n"
            report += f"  Reason: {log['reason']}\n\n"
        
        return report
    
    def create_access_summary_chart(self, frame):
        """Create a chart summarizing access attempts (granted vs. denied)"""
        logs = self.model.access_logs
        
        # Count granted and denied access attempts
        granted = sum(1 for log in logs if log['access_granted'])
        denied = len(logs) - granted
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(['Granted', 'Denied'], [granted, denied], color=['green', 'red'])
        ax.set_title('Access Attempts Summary')
        ax.set_ylabel('Number of Attempts')
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        
        return canvas.get_tk_widget()
    
    def create_company_access_chart(self, frame):
        """Create a chart showing access attempts by company"""
        logs = self.model.access_logs
        
        # Count access attempts by company
        company_access = {}
        for log in logs:
            company = log['company_name']
            if company not in company_access:
                company_access[company] = {'granted': 0, 'denied': 0}
            
            if log['access_granted']:
                company_access[company]['granted'] += 1
            else:
                company_access[company]['denied'] += 1
        
        # Prepare data for plotting
        companies = list(company_access.keys())
        granted = [company_access[company]['granted'] for company in companies]
        denied = [company_access[company]['denied'] for company in companies]
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(8, 5))
        
        # Create stacked bar chart
        ax.bar(companies, granted, label='Granted', color='green')
        ax.bar(companies, denied, bottom=granted, label='Denied', color='red')
        
        ax.set_title('Access Attempts by Company')
        ax.set_ylabel('Number of Attempts')
        ax.set_xlabel('Company')
        ax.legend()
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        
        return canvas.get_tk_widget()
    
    def create_user_access_chart(self, frame):
        """Create a chart showing access attempts by user"""
        logs = self.model.access_logs
        
        # Count access attempts by user
        user_access = {}
        for log in logs:
            user = log['user_name']
            if user not in user_access:
                user_access[user] = {'granted': 0, 'denied': 0}
            
            if log['access_granted']:
                user_access[user]['granted'] += 1
            else:
                user_access[user]['denied'] += 1
        
        # Prepare data for plotting
        users = list(user_access.keys())
        granted = [user_access[user]['granted'] for user in users]
        denied = [user_access[user]['denied'] for user in users]
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(8, 5))
        
        # Create stacked bar chart
        ax.bar(users, granted, label='Granted', color='green')
        ax.bar(users, denied, bottom=granted, label='Denied', color='red')
        
        ax.set_title('Access Attempts by User')
        ax.set_ylabel('Number of Attempts')
        ax.set_xlabel('User')
        ax.legend()
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        
        return canvas.get_tk_widget()
    
    def visualize_coi_structure(self, frame):
        """Create a visualization of the COI structure"""
        structure = self.model.get_coi_structure()
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Prepare data for plotting
        coi_positions = {}
        company_positions = {}
        
        # Position COI classes horizontally
        num_coi = len(structure)
        for i, coi in enumerate(structure):
            coi_x = i * 10
            coi_positions[coi['coi_class_id']] = coi_x
            
            # Position companies within each COI class
            companies = coi['companies']
            for j, company in enumerate(companies):
                company_x = coi_x
                company_y = j * 5
                company_positions[company['id']] = (company_x, company_y)
        
        # Plot COI classes
        for coi_id, x_pos in coi_positions.items():
            ax.annotate(f"COI Class: {coi_id}", xy=(x_pos, -5), fontsize=12, ha='center')
            
            # Draw rectangle around companies in this COI class
            companies = [c for coi in structure if coi['coi_class_id'] == coi_id for c in coi['companies']]
            if companies:
                min_y = min(company_positions[c['id']][1] for c in companies) - 2
                max_y = max(company_positions[c['id']][1] for c in companies) + 2
                rect = plt.Rectangle((x_pos - 4, min_y), 8, max_y - min_y, fill=False, edgecolor='blue', linestyle='--')
                ax.add_patch(rect)
        
        # Plot companies
        for company_id, (x, y) in company_positions.items():
            company_name = next((c['name'] for coi in structure for c in coi['companies'] if c['id'] == company_id), company_id)
            ax.scatter(x, y, s=100, color='green')
            ax.annotate(company_name, xy=(x, y), xytext=(x + 1, y), fontsize=10)
        
        # Set plot limits and labels
        ax.set_xlim(-5, max(pos for pos in coi_positions.values()) + 10)
        ax.set_ylim(-10, max(pos[1] for pos in company_positions.values()) + 10)
        ax.set_title('Chinese Wall Model Structure')
        ax.set_xlabel('Conflict of Interest Classes')
        ax.set_yticks([])
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        
        return canvas.get_tk_widget()
