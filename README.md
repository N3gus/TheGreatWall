# Chinese Wall Model Demonstration

This application demonstrates the Chinese Wall Model, a security policy model used to prevent conflicts of interest in commercial organizations.

## Overview

The Chinese Wall Model is designed to prevent information flows that could cause conflicts of interest. It dynamically builds walls between datasets as users access information, preventing access to conflicting information.

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
- Ability to add/modify datasets and users

## Usage
1. Run the application: `python chinese_wall_app.py`
2. Log in with one of the provided test users
3. Attempt to access different datasets to see the Chinese Wall Model in action
4. Generate reports to review access patterns and violations

## Requirements
- Python 3.6+
- Tkinter (included in standard Python distribution)
- Matplotlib (for visualization)
