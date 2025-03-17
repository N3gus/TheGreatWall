"""
Utility functions for the Chinese Wall Model Application
"""

import tkinter as tk
from tkinter import ttk
import random

def create_tooltip(widget, text):
    """Create a tooltip for a widget"""
    def enter(event):
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25
        
        # Create a toplevel window
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{x}+{y}")
        
        # Create label in the toplevel
        label = ttk.Label(tooltip, text=text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("Arial", "10", "normal"))
        label.pack(ipadx=5, ipady=5)
        
        # Store the tooltip reference
        widget.tooltip = tooltip
    
    def leave(event):
        if hasattr(widget, "tooltip"):
            widget.tooltip.destroy()
    
    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)

def center_window(window, width, height):
    """Center a window on the screen"""
    # Get screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Calculate position
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # Set window size and position
    window.geometry(f'{width}x{height}+{x}+{y}')

def create_scrollable_frame(parent):
    """Create a scrollable frame"""
    # Create a canvas
    canvas = tk.Canvas(parent)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Add a scrollbar to the canvas
    scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Configure the canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    # Create a frame inside the canvas
    frame = ttk.Frame(canvas)
    
    # Add the frame to the canvas
    canvas.create_window((0, 0), window=frame, anchor="nw")
    
    return frame

def create_styled_button(parent, text, command, **kwargs):
    """Create a styled button"""
    style_name = f"Custom.TButton.{random.randint(1000, 9999)}"
    style = ttk.Style()
    style.configure(style_name, font=('Arial', 10), padding=5)
    
    button = ttk.Button(parent, text=text, command=command, style=style_name, **kwargs)
    return button

def create_section_header(parent, text):
    """Create a section header"""
    frame = ttk.Frame(parent)
    frame.pack(fill=tk.X, padx=5, pady=5)
    
    label = ttk.Label(frame, text=text, font=('Arial', 12, 'bold'))
    label.pack(anchor=tk.W)
    
    separator = ttk.Separator(frame, orient=tk.HORIZONTAL)
    separator.pack(fill=tk.X, pady=5)
    
    return frame

def create_info_box(parent, title, content):
    """Create an information box"""
    frame = ttk.LabelFrame(parent, text=title)
    frame.pack(fill=tk.X, padx=10, pady=5, ipady=5)
    
    label = ttk.Label(frame, text=content, wraplength=400, justify=tk.LEFT)
    label.pack(padx=10, pady=5)
    
    return frame

def format_access_result(result, reason):
    """Format access result for display"""
    if result:
        return f"✅ Access Granted: {reason}"
    else:
        return f"❌ Access Denied: {reason}"

def explain_chinese_wall():
    """Return an explanation of the Chinese Wall Model"""
    explanation = """
The Chinese Wall Model is a security policy model used to prevent conflicts of interest in commercial organizations.

Key concepts:
1. Conflict of Interest (COI) Classes: Groups of competing companies (e.g., different banks)
2. Company Datasets: Information about specific companies
3. Objects: Individual data items belonging to company datasets

Rules:
1. A user can initially access any company's data
2. Once a user accesses data from a company, they cannot access data from any competing company
3. The user can still access data from companies in different COI classes
4. Access rights are dynamically determined based on the user's access history

This model is particularly useful in financial and consulting sectors where analysts must be prevented from accessing information that could create conflicts of interest.
"""
    return explanation

def explain_coi_classes():
    """Return an explanation of Conflict of Interest Classes"""
    explanation = """
Conflict of Interest (COI) Classes are groups of companies that compete with each other in the same market sector.

For example:
- Banking COI Class: Global Bank, National Finance, City Credit Union
- Oil COI Class: Petrol Giant, Oceanic Oil, Energy Solutions
- Tech COI Class: MegaSoft, Fruit Computers, Search Engine Inc

The Chinese Wall Model prevents a user who has accessed data from one company in a COI class from accessing data from any other company in the same COI class.

This prevents potential conflicts of interest by ensuring users cannot use inside information from one company to benefit a competitor.
"""
    return explanation
