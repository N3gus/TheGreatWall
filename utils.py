"""
Utility functions for the Chinese Wall Model Application
"""

import tkinter as tk
from tkinter import ttk, font
import random
from typing import Optional, Callable, Dict, Any, List, Tuple
import platform

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
        
        # Add border and shadow effect
        tooltip.configure(background="#2a2a2a", bd=1)
        
        # Create label in the toplevel
        label = ttk.Label(tooltip, text=text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("Arial", "10", "normal"), wraplength=300)
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
    canvas = tk.Canvas(parent, borderwidth=0, highlightthickness=0)
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
    
    # Add mouse wheel scrolling
    def _on_mousewheel(event):
        # Cross-platform mouse wheel scrolling
        if platform.system() == 'Windows':
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        else:
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")
    
    # Bind mousewheel events
    if platform.system() == 'Windows':
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    else:
        canvas.bind_all("<Button-4>", _on_mousewheel)
        canvas.bind_all("<Button-5>", _on_mousewheel)
    
    return frame

def create_styled_button(parent, text, command, **kwargs):
    """Create a styled button"""
    style_name = f"Custom.TButton.{random.randint(1000, 9999)}"
    style = ttk.Style()
    
    # Default styling
    padding = kwargs.pop('padding', 5)
    font_size = kwargs.pop('font_size', 10)
    font_weight = kwargs.pop('font_weight', 'normal')
    
    style.configure(style_name, 
                   font=('Arial', font_size, font_weight), 
                   padding=padding)
    
    button = ttk.Button(parent, text=text, command=command, style=style_name, **kwargs)
    return button

def create_section_header(parent, text):
    """Create a section header"""
    frame = ttk.Frame(parent)
    frame.pack(fill=tk.X, padx=5, pady=5)
    
    label = ttk.Label(frame, text=text, font=('Arial', 12, 'bold'), foreground="#1976d2")
    label.pack(anchor=tk.W)
    
    separator = ttk.Separator(frame, orient=tk.HORIZONTAL)
    separator.pack(fill=tk.X, pady=5)
    
    return frame

def create_info_box(parent, title, content, **kwargs):
    """Create an information box"""
    bg_color = kwargs.pop('bg_color', '#e3f2fd')  # Light blue background
    text_color = kwargs.pop('text_color', '#000000')
    border_color = kwargs.pop('border_color', '#1976d2')
    
    # Create a frame with custom styling
    frame = tk.Frame(parent, bg=border_color, padx=2, pady=2)
    frame.pack(fill=tk.X, padx=10, pady=5)
    
    # Inner frame with background color
    inner_frame = tk.Frame(frame, bg=bg_color)
    inner_frame.pack(fill=tk.BOTH, expand=True)
    
    # Title
    if title:
        title_label = tk.Label(inner_frame, text=title, font=('Arial', 11, 'bold'),
                              bg=bg_color, fg=text_color)
        title_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
    
    # Content
    content_label = tk.Label(inner_frame, text=content, wraplength=kwargs.get('wraplength', 400),
                            justify=tk.LEFT, bg=bg_color, fg=text_color)
    content_label.pack(padx=10, pady=(0, 10), anchor=tk.W)
    
    return frame

def format_access_result(result, reason):
    """Format access result for display"""
    if result:
        return f"✅ Access Granted: {reason}"
    else:
        return f"❌ Access Denied: {reason}"

def create_card(parent, title, content=None, **kwargs):
    """Create a card-like UI element with optional content"""
    # Card styling
    bg_color = kwargs.pop('bg_color', '#ffffff')
    border_color = kwargs.pop('border_color', '#e0e0e0')
    title_bg = kwargs.pop('title_bg', '#f5f5f5')
    
    # Create main frame with border
    card_frame = tk.Frame(parent, bg=border_color, bd=1)
    card_frame.pack(fill=tk.X, padx=10, pady=10, ipadx=1, ipady=1)
    
    # Title section
    title_frame = tk.Frame(card_frame, bg=title_bg)
    title_frame.pack(fill=tk.X)
    
    title_label = tk.Label(title_frame, text=title, bg=title_bg,
                          font=('Arial', 11, 'bold'), anchor='w')
    title_label.pack(fill=tk.X, padx=10, pady=8)
    
    # Content section if provided
    if content:
        content_frame = tk.Frame(card_frame, bg=bg_color)
        content_frame.pack(fill=tk.X)
        
        if isinstance(content, str):
            # String content
            content_label = tk.Label(content_frame, text=content, bg=bg_color,
                                    justify=tk.LEFT, wraplength=kwargs.get('wraplength', 400))
            content_label.pack(fill=tk.X, padx=10, pady=10, anchor='w')
        else:
            # Assume content is a widget or frame to be packed
            content.pack(fill=tk.X, padx=10, pady=10)
    
    # Return the content frame for adding additional widgets
    return card_frame

def create_data_table(parent, headers, data, **kwargs):
    """Create a table-like display for data"""
    # Create a frame for the table
    table_frame = ttk.Frame(parent)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # Configure style for the treeview
    style = ttk.Style()
    style.configure("Treeview", font=('Arial', 10))
    style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
    
    # Create the treeview with columns
    tree = ttk.Treeview(table_frame, columns=headers, show='headings', 
                       selectmode='browse', **kwargs)
    
    # Configure the columns and headings
    for i, header in enumerate(headers):
        tree.heading(i, text=header)
        tree.column(i, width=font.Font().measure(header) + 20)
    
    # Insert the data
    for row in data:
        tree.insert('', 'end', values=row)
    
    # Add scrollbars
    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    # Grid layout
    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')
    
    table_frame.grid_columnconfigure(0, weight=1)
    table_frame.grid_rowconfigure(0, weight=1)
    
    return tree

def create_notification(parent, message, notification_type='info', duration=3000):
    """Create a temporary notification that disappears after a duration"""
    # Colors based on notification type
    colors = {
        'info': ('#e3f2fd', '#1976d2'),  # Light blue bg, blue text
        'success': ('#e8f5e9', '#2e7d32'),  # Light green bg, green text
        'warning': ('#fff8e1', '#f57c00'),  # Light yellow bg, orange text
        'error': ('#ffebee', '#c62828')  # Light red bg, red text
    }
    
    bg_color, text_color = colors.get(notification_type, colors['info'])
    
    # Create a toplevel window
    notification = tk.Toplevel(parent)
    notification.wm_overrideredirect(True)
    
    # Position at the top center of the parent window
    x = parent.winfo_rootx() + parent.winfo_width() // 2 - 150
    y = parent.winfo_rooty() + 50
    notification.geometry(f"300x80+{x}+{y}")
    
    # Create a frame with border
    frame = tk.Frame(notification, bg=text_color, bd=1)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Inner frame with background color
    inner_frame = tk.Frame(frame, bg=bg_color)
    inner_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
    
    # Message label
    label = tk.Label(inner_frame, text=message, bg=bg_color, fg=text_color,
                    font=('Arial', 10), wraplength=280, justify=tk.LEFT)
    label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    # Close button
    close_button = tk.Label(inner_frame, text="×", bg=bg_color, fg=text_color,
                           font=('Arial', 14, 'bold'), cursor="hand2")
    close_button.place(relx=1.0, x=-10, y=5, anchor="ne")
    close_button.bind("<Button-1>", lambda e: notification.destroy())
    
    # Auto-close after duration
    notification.after(duration, notification.destroy)
    
    return notification

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

def create_badge(parent, text, **kwargs):
    """Create a badge-style label"""
    bg_color = kwargs.pop('bg_color', '#1976d2')  # Default blue
    fg_color = kwargs.pop('fg_color', 'white')
    font_size = kwargs.pop('font_size', 9)
    
    badge = tk.Label(parent, text=text, bg=bg_color, fg=fg_color,
                    font=('Arial', font_size), padx=6, pady=1,
                    borderwidth=0, relief="flat", **kwargs)
    
    # Round corners effect (limited in tkinter, but we can try)
    return badge

def create_collapsible_section(parent, title, content_creator_func):
    """Create a collapsible section that can be expanded/collapsed"""
    # Main frame
    frame = ttk.Frame(parent)
    frame.pack(fill=tk.X, padx=5, pady=2)
    
    # Header frame with button
    header_frame = ttk.Frame(frame)
    header_frame.pack(fill=tk.X)
    
    # State variables
    is_expanded = tk.BooleanVar(value=False)
    content_frame = None
    
    def toggle():
        if is_expanded.get():
            # Collapse
            if content_frame:
                content_frame.pack_forget()
            is_expanded.set(False)
            toggle_button.configure(text="▶")
        else:
            # Expand
            nonlocal content_frame
            content_frame = ttk.Frame(frame)
            content_frame.pack(fill=tk.X, padx=20, pady=5)
            content_creator_func(content_frame)
            is_expanded.set(True)
            toggle_button.configure(text="▼")
    
    # Toggle button
    toggle_button = ttk.Label(header_frame, text="▶", cursor="hand2")
    toggle_button.pack(side=tk.LEFT, padx=(0, 5))
    toggle_button.bind("<Button-1>", lambda e: toggle())
    
    # Title
    title_label = ttk.Label(header_frame, text=title, font=('Arial', 11, 'bold'))
    title_label.pack(side=tk.LEFT)
    title_label.bind("<Button-1>", lambda e: toggle())
    
    # Make the entire header clickable
    header_frame.bind("<Button-1>", lambda e: toggle())
    
    return frame

def is_dark_mode():
    """Detect if the system is using dark mode (limited functionality)"""
    # This is a simple approximation and may not work on all systems
    if platform.system() == 'Windows':
        try:
            import winreg
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return value == 0
        except:
            return False
    elif platform.system() == 'Darwin':  # macOS
        try:
            import subprocess
            result = subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'], 
                                   capture_output=True, text=True)
            return 'Dark' in result.stdout
        except:
            return False
    else:
        return False  # Default to light mode on other platforms

def adapt_color_to_theme(light_color, dark_color):
    """Return the appropriate color based on system theme"""
    if is_dark_mode():
        return dark_color
    return light_color
