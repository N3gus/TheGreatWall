# The Great Wall: Chinese Wall Security Model Demonstration

This application demonstrates the Chinese Wall Security Model, a security policy used to prevent conflicts of interest in commercial organizations.

## Overview

The Chinese Wall Security Model is designed to prevent information flows that could cause conflicts of interest. It dynamically builds walls between datasets as users access information, preventing access to conflicting information.

Key concepts:
- **Conflict of Interest Classes**: Groups of company datasets that compete with each other
- **Company Datasets**: Information about specific companies
- **Objects**: Individual data items belonging to company datasets

## Features
- User authentication and role management
- Dynamic enforcement of Chinese Wall access controls
- Real-time feedback on access attempts
- Visualization of conflict-of-interest relationships
- Report generation for audit purposes
- Admin interface for managing users, companies, and COI classes
- Help screen with explanations of the Chinese Wall model

## Project Structure
- `chinese_wall_model.py` - Core implementation of the Chinese Wall security model
- `data_manager.py` - Manages data initialization and operations
- `gui_app.py` - Main application entry point with Tkinter GUI
- `report_generator.py` - Generates reports and visualizations
- `utils.py` - Utility functions for the GUI
- Various screen modules:
  - `login_screen.py` - User authentication interface
  - `main_dashboard.py` - Main user interface for accessing data
  - `report_screen.py` - Interface for generating and viewing reports
  - `admin_screen.py` - Interface for administrative functions
  - `help_screen.py` - Information about the Chinese Wall model

## Sample Data
The application comes pre-loaded with sample data including:
- 3 Conflict of Interest Classes: Banking, Oil Companies, and Technology Companies
- 3 Companies in each COI class
- Multiple data objects for each company
- Sample users with different roles

## Usage
1. Run the application: `python gui_app.py`
2. Log in with one of the provided test users
3. Attempt to access different datasets to see the Chinese Wall Model in action
4. Generate reports to review access patterns and violations
5. Use the admin interface to manage users, companies, and data (if you have admin privileges)

## Requirements
- Python 3.6+
- Tkinter (included in standard Python distribution)
- Matplotlib (for visualization)
- NumPy (for data processing)
- Pillow (for image handling)

## Installation
```
pip install matplotlib numpy pillow
```

## Educational Purpose
This application is designed for educational purposes to demonstrate the principles and implementation of the Chinese Wall Security Model in a practical, interactive way.
