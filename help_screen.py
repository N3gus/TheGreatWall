"""
Help Screen Component
Provides educational content about the Chinese Wall Model
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from utils import create_tooltip, center_window

class HelpScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create the widgets for the help screen"""
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(header_frame, text="Chinese Wall Model Help", 
                 font=('Arial', 16, 'bold')).pack(side=tk.LEFT)
        
        # Back button
        back_button = ttk.Button(header_frame, text="Back to Dashboard", 
                                command=lambda: self.controller.show_frame("MainDashboard"))
        back_button.pack(side=tk.RIGHT)
        
        # Create a notebook for different help sections
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create tabs for different help sections
        self.create_overview_tab()
        self.create_concepts_tab()
        self.create_tutorial_tab()
        self.create_faq_tab()
        self.create_about_tab()
    
    def create_overview_tab(self):
        """Create the overview tab"""
        overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(overview_frame, text="Overview")
        
        # Overview content
        content = scrolledtext.ScrolledText(overview_frame, wrap=tk.WORD, 
                                           font=('Arial', 11), padx=10, pady=10)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Make the text read-only
        content.config(state=tk.NORMAL)
        
        # Add the overview content
        overview_text = """
# Chinese Wall Model Overview

## What is the Chinese Wall Model?

The Chinese Wall Model is a security model used to prevent conflicts of interest in organizations, particularly in financial and consulting firms. It was formally defined by Brewer and Nash in 1989 as a security policy that combines commercial discretion with legally enforceable mandatory controls.

## Purpose of this Application

This application is designed to demonstrate the principles and operation of the Chinese Wall Model in an interactive and educational way. It allows users to:

1. Understand how the Chinese Wall Model works through practical examples
2. Experience the access control mechanisms that enforce the model
3. Visualize the conflicts of interest and how they are managed
4. Learn about the theoretical foundations of the model

## Key Features

- **User Simulation**: Experience the model from different user perspectives
- **Access Control**: See how access decisions are made in real-time
- **Visual Representation**: Graphical display of conflict of interest classes and companies
- **Reports and Analytics**: Generate reports on access patterns and potential conflicts
- **Administrative Tools**: Manage users, companies, and conflict of interest classes

## Getting Started

To begin exploring the Chinese Wall Model:

1. Log in using one of the provided user accounts
2. Navigate to the main dashboard to view available companies and their data
3. Attempt to access different company data to see how the model enforces access control
4. View your access history to understand your "contamination" status
5. Generate reports to analyze access patterns

## Educational Value

This application serves as an educational tool for:
- Information security students and professionals
- Compliance officers and regulatory professionals
- Anyone interested in access control models and information flow security

By interacting with this application, you'll gain a deeper understanding of how the Chinese Wall Model balances the need for information sharing with the requirement to prevent conflicts of interest.
"""
        content.insert(tk.END, overview_text)
        content.config(state=tk.DISABLED)
    
    def create_concepts_tab(self):
        """Create the concepts tab"""
        concepts_frame = ttk.Frame(self.notebook)
        self.notebook.add(concepts_frame, text="Key Concepts")
        
        # Concepts content
        content = scrolledtext.ScrolledText(concepts_frame, wrap=tk.WORD, 
                                           font=('Arial', 11), padx=10, pady=10)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Make the text read-only
        content.config(state=tk.NORMAL)
        
        # Add the concepts content
        concepts_text = """
# Key Concepts of the Chinese Wall Model

## Core Principles

The Chinese Wall Model is based on the following key principles:

### 1. Conflict of Interest Classes (COI)

- A COI class contains companies that are in competition with each other
- For example, all banks might be in one COI class, all oil companies in another
- Access to information about one company in a COI class prevents access to information about any other company in the same class

### 2. Company Datasets

- Each company has its own dataset containing sensitive information
- These datasets are what the Chinese Wall Model aims to protect
- Access to these datasets is controlled based on the user's access history

### 3. Access Control Rules

The Chinese Wall Model enforces two main rules:

- **Simple Security Rule**: A subject can access an object if and only if:
  - The object is in the same company dataset as an object already accessed by the subject, OR
  - The object belongs to a company dataset in an entirely different conflict of interest class

- ***-Property (Star Property)**: A subject can write to an object if and only if:
  - The subject cannot read any object containing unsanitized information from a different company dataset, AND
  - The subject cannot read any object from a company dataset in a different COI class

### 4. Information Flow

- The model prevents information flow that could create conflicts of interest
- Once a user accesses information from one company, they are "contaminated" with respect to competitors
- This contamination restricts future access to prevent potential conflicts

### 5. Sanitized Information

- Some information can be marked as "sanitized" (free from sensitive details)
- Sanitized information can be accessed without the same restrictions
- This allows for necessary information sharing while maintaining security

## Practical Implementation

In this application, we implement these concepts as follows:

- **COI Classes**: Represented as categories of companies (e.g., Banking, Oil, Retail)
- **Companies**: Organizations within each COI class with their own datasets
- **Objects**: Individual data items belonging to companies
- **Access History**: Tracking which companies' data each user has accessed
- **Access Control**: Enforcing the Chinese Wall rules based on access history

## Real-World Applications

The Chinese Wall Model is commonly used in:

- Investment banks separating trading and advisory functions
- Consulting firms managing multiple clients in the same industry
- Law firms handling cases with potential conflicts
- Regulatory bodies with access to sensitive industry information

By understanding these concepts, you'll be better equipped to navigate the application and appreciate how the Chinese Wall Model works in practice.
"""
        content.insert(tk.END, concepts_text)
        content.config(state=tk.DISABLED)
    
    def create_tutorial_tab(self):
        """Create the tutorial tab"""
        tutorial_frame = ttk.Frame(self.notebook)
        self.notebook.add(tutorial_frame, text="Tutorial")
        
        # Tutorial content
        content = scrolledtext.ScrolledText(tutorial_frame, wrap=tk.WORD, 
                                           font=('Arial', 11), padx=10, pady=10)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Make the text read-only
        content.config(state=tk.NORMAL)
        
        # Add the tutorial content
        tutorial_text = """
# Tutorial: Using the Chinese Wall Model Application

This tutorial will guide you through the main features of the application and how to use them effectively.

## 1. Logging In

When you start the application, you'll see the login screen:

1. Select a user from the dropdown menu
2. Click "Login" to enter the application
3. Note the introduction to the Chinese Wall Model on this screen

## 2. Navigating the Main Dashboard

After logging in, you'll see the main dashboard:

1. The left panel shows available companies grouped by their Conflict of Interest (COI) class
2. The right panel displays your access history and current "contamination" status
3. The top menu provides navigation to other screens (Reports, Admin, Help)

## 3. Accessing Company Data

To access company data:

1. Click on a company in the left panel
2. If access is allowed (based on Chinese Wall rules), you'll see the company's data
3. If access is denied, you'll see an explanation of why (based on your access history)
4. Notice how your access history updates after successful access

## 4. Understanding Access Control

To experience the Chinese Wall Model in action:

1. First, access data from one company (e.g., Bank A)
2. Then, try to access data from a competitor (e.g., Bank B)
3. You'll be denied access because they're in the same COI class
4. However, you can still access data from a company in a different COI class (e.g., Oil X)

## 5. Viewing Reports

To generate and view reports:

1. Click on "Reports" in the top menu
2. Select the type of report you want to generate
3. View statistics and visualizations about access patterns
4. Export reports if needed

## 6. Administrative Functions

If you have admin privileges:

1. Click on "Admin" in the top menu
2. Navigate between the tabs for User Management, Company Management, and COI Class Management
3. Add, edit, or delete users, companies, and COI classes
4. Manage company data objects

## 7. Getting Help

If you need assistance:

1. Click on "Help" in the top menu
2. Browse the different tabs for information about the model and application
3. Refer to the FAQ section for common questions

## 8. Logging Out

When you're finished:

1. Click on "Logout" in the top menu
2. You'll be returned to the login screen

## Practice Scenario

Try this scenario to understand the Chinese Wall Model:

1. Log in as "Alice"
2. Access data from "Bank A"
3. Try to access data from "Bank B" (should be denied)
4. Access data from "Oil X" (should be allowed)
5. Log out and log in as "Bob"
6. Notice Bob has a different access history
7. Try accessing various companies to see how the rules apply

By following this tutorial, you'll gain hands-on experience with the Chinese Wall Model and understand how it prevents conflicts of interest while allowing necessary information access.
"""
        content.insert(tk.END, tutorial_text)
        content.config(state=tk.DISABLED)
    
    def create_faq_tab(self):
        """Create the FAQ tab"""
        faq_frame = ttk.Frame(self.notebook)
        self.notebook.add(faq_frame, text="FAQ")
        
        # FAQ content
        content = scrolledtext.ScrolledText(faq_frame, wrap=tk.WORD, 
                                           font=('Arial', 11), padx=10, pady=10)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Make the text read-only
        content.config(state=tk.NORMAL)
        
        # Add the FAQ content
        faq_text = """
# Frequently Asked Questions

## General Questions

### Q: What is the purpose of this application?
**A:** This application is designed to demonstrate the Chinese Wall Model of access control in an interactive and educational way. It helps users understand how conflicts of interest are managed in organizations that handle sensitive information from competing entities.

### Q: Is this application used in real-world scenarios?
**A:** This specific application is for educational purposes. However, the principles it demonstrates are widely used in financial institutions, consulting firms, and other organizations that need to manage conflicts of interest.

### Q: Can I use this application for my own organization?
**A:** While this application is primarily educational, the code could be adapted for real-world use with appropriate modifications for security, scalability, and specific organizational needs.

## Chinese Wall Model Questions

### Q: How is the Chinese Wall Model different from other access control models?
**A:** Unlike traditional access control models (like Role-Based Access Control or Mandatory Access Control), the Chinese Wall Model is dynamic - access permissions change based on a user's access history. It specifically addresses conflicts of interest rather than just confidentiality or integrity.

### Q: Does the Chinese Wall Model prevent all conflicts of interest?
**A:** The model prevents conflicts within its defined rules, but real-world implementations require additional policies, training, and oversight. The model addresses information access conflicts but not all types of conflicts of interest.

### Q: What are the limitations of the Chinese Wall Model?
**A:** The model can be restrictive in organizations where collaboration is needed. It also doesn't address temporal conflicts (where access at different times might still create conflicts) without additional controls. Implementation can be complex in large organizations.

## Application Usage

### Q: Why can't I access certain company data?
**A:** If you've previously accessed data from a company in the same Conflict of Interest (COI) class, the Chinese Wall Model prevents you from accessing competitor data to avoid conflicts of interest.

### Q: How do I reset my access history?
**A:** In a real-world implementation, access history typically isn't reset as it would defeat the purpose of the model. In this educational application, you can log out and log in as a different user to experience different access patterns.

### Q: What do the different colors in the reports mean?
**A:** In the visualizations, different colors typically represent different COI classes or access statuses. Green often indicates allowed access, red indicates denied access, and different colors in charts represent different categories or classes.

### Q: Can I add my own companies and COI classes?
**A:** Yes, if you have administrative privileges, you can add, edit, and delete companies and COI classes through the Admin screen.

## Technical Questions

### Q: What technologies are used to build this application?
**A:** This application is built using Python with the Tkinter library for the graphical user interface. It also uses matplotlib for visualizations in the reports section.

### Q: Is my data saved between sessions?
**A:** In this educational version, data is initialized with sample values each time the application starts and is not persisted between sessions. A production version would include database integration.

### Q: How can I extend the application's functionality?
**A:** The application is designed with a modular architecture. You can modify or extend the code to add new features, integrate with databases, or customize the user interface as needed.

### Q: Where can I learn more about the Chinese Wall Model?
**A:** The original paper by Brewer and Nash (1989) titled "The Chinese Wall Security Policy" is a good starting point. Additionally, information security textbooks and academic papers on access control models often cover the Chinese Wall Model.
"""
        content.insert(tk.END, faq_text)
        content.config(state=tk.DISABLED)
    
    def create_about_tab(self):
        """Create the about tab"""
        about_frame = ttk.Frame(self.notebook)
        self.notebook.add(about_frame, text="About")
        
        # About content
        content = scrolledtext.ScrolledText(about_frame, wrap=tk.WORD, 
                                           font=('Arial', 11), padx=10, pady=10)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Make the text read-only
        content.config(state=tk.NORMAL)
        
        # Add the about content
        about_text = """
# About This Application

## The Great Wall: Chinese Wall Model Demonstration

### Version 1.0

This application was developed as an educational tool to demonstrate the principles and operation of the Chinese Wall Security Model, a fundamental concept in information security and access control.

### Purpose

The primary purpose of this application is to provide an interactive learning environment for:

- Students studying information security concepts
- Professionals seeking to understand conflict of interest management
- Educators teaching access control models
- Anyone interested in security policies and their implementation

### Features

- Interactive demonstration of Chinese Wall Model principles
- Simulated environment with users, companies, and conflict of interest classes
- Real-time access control decisions based on user history
- Visual representations of access patterns and conflicts
- Administrative tools for managing the simulation environment

### The Chinese Wall Model

The Chinese Wall Security Model was formally introduced by Brewer and Nash in their 1989 paper "The Chinese Wall Security Policy" published in the IEEE Symposium on Security and Privacy. It addresses the specific problem of preventing conflicts of interest in organizations that deal with competing entities.

The model is named after the "Chinese Wall" concept used in financial and legal firms to separate departments that might have conflicts of interest. It combines aspects of mandatory and discretionary access control in a dynamic way that depends on user access history.

### Educational Value

This application helps bridge the gap between theoretical understanding and practical implementation of the Chinese Wall Model by:

1. Providing hands-on experience with the model's rules
2. Visualizing the impact of access decisions
3. Demonstrating how conflicts of interest are prevented
4. Showing the administrative aspects of maintaining such a system

### Development

This application was developed using Python and Tkinter, with a focus on creating a clear, intuitive interface that highlights the key concepts of the Chinese Wall Model.

### Feedback and Contributions

This is an educational project and feedback is welcome. If you have suggestions for improvements or would like to contribute to the development, please contact the development team.

### Acknowledgments

- Brewer and Nash for their original formulation of the Chinese Wall Model
- The information security community for ongoing research and education in access control models
- All contributors to the open-source libraries used in this application

### License

This application is provided for educational purposes. All code and content are available for educational use and modification with appropriate attribution.

© 2023 The Great Wall Development Team
"""
        content.insert(tk.END, about_text)
        content.config(state=tk.DISABLED)
