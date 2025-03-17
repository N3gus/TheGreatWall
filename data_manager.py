"""
Data Manager for Chinese Wall Model Application
Handles initialization and management of sample data for the application
"""

from datetime import datetime

class DataManager:
    def __init__(self, model):
        """Initialize with a reference to the ChineseWallModel instance"""
        self.model = model
    
    def initialize_sample_data(self):
        """Initialize the model with sample data for demonstration"""
        # Create Conflict of Interest Classes
        self.model.add_coi_class("banking", "Banking")
        self.model.add_coi_class("oil", "Oil Companies")
        self.model.add_coi_class("tech", "Technology Companies")
        
        # Add companies to Banking COI class
        self.model.add_company("bank1", "Global Bank", "banking")
        self.model.add_company("bank2", "National Finance", "banking")
        self.model.add_company("bank3", "Bank Of Zambia", "banking")
        
        # Add companies to Oil COI class
        self.model.add_company("oil1", "Petrol Giant", "oil")
        self.model.add_company("oil2", "Oceanic Oil", "oil")
        self.model.add_company("oil3", "Energy Solutions", "oil")
        
        # Add companies to Tech COI class
        self.model.add_company("tech1", "MegaSoft", "tech")
        self.model.add_company("tech2", "Fruit Computers", "tech")
        self.model.add_company("tech3", "Search Engine Inc", "tech")
        
        # Add objects (data) to companies
        # Banking data
        self.model.add_object("bank1", "financial_report", "Annual financial report showing 12% growth")
        self.model.add_object("bank1", "merger_plans", "Confidential plans for merger with smaller banks")
        self.model.add_object("bank1", "customer_data", "Encrypted database of customer information")
        
        self.model.add_object("bank2", "investment_strategy", "Long-term investment strategy document")
        self.model.add_object("bank2", "risk_assessment", "Risk assessment for Q3 2024")
        self.model.add_object("bank2", "board_minutes", "Minutes from board meeting on March 1, 2024")
        
        self.model.add_object("bank3", "loan_portfolio", "Analysis of current loan portfolio")
        self.model.add_object("bank3", "expansion_plans", "Plans to open 5 new branches in 2025")
        self.model.add_object("bank3", "interest_rates", "Internal document on interest rate adjustments")
        
        # Oil company data
        self.model.add_object("oil1", "drilling_report", "Report on new drilling sites in the Pacific")
        self.model.add_object("oil1", "environmental_study", "Environmental impact study for Arctic operations")
        self.model.add_object("oil1", "production_forecast", "Oil production forecast for next 5 years")
        
        self.model.add_object("oil2", "acquisition_targets", "List of potential acquisition targets")
        self.model.add_object("oil2", "refinery_specs", "Technical specifications for new refinery")
        self.model.add_object("oil2", "supply_contracts", "Details of supply contracts with Asian markets")
        
        self.model.add_object("oil3", "renewable_investment", "Investment plans for renewable energy division")
        self.model.add_object("oil3", "executive_compensation", "Executive compensation packages")
        self.model.add_object("oil3", "strategic_pivot", "Strategic pivot to green energy technologies")
        
        # Tech company data
        self.model.add_object("tech1", "product_roadmap", "Product roadmap for next 3 years")
        self.model.add_object("tech1", "research_budget", "R&D budget allocation for AI initiatives")
        self.model.add_object("tech1", "competitor_analysis", "Analysis of market competitors")
        
        self.model.add_object("tech2", "device_specs", "Specifications for upcoming device releases")
        self.model.add_object("tech2", "supply_chain", "Supply chain optimization strategy")
        self.model.add_object("tech2", "patent_applications", "Recent patent applications for display technology")
        
        self.model.add_object("tech3", "algorithm_update", "Documentation for search algorithm update")
        self.model.add_object("tech3", "ad_platform", "New advertising platform specifications")
        self.model.add_object("tech3", "user_data_policy", "Internal policy on user data handling")
        
        # Add users
        self.model.add_user("user1", "Nkusechela Siame", "consultant")
        self.model.add_user("user2", "Mweetwa Nketani", "analyst")
        self.model.add_user("user3", "Tshaka Zulu", "manager")
        self.model.add_user("user4", "Emmanuel Mwale", "auditor")
        self.model.add_user("admin", "Tiness Kamwale", "administrator")
    
    def add_new_company(self, company_id, name, coi_class_id):
        """Add a new company to the system"""
        return self.model.add_company(company_id, name, coi_class_id)
    
    def add_new_object(self, company_id, object_id, object_data):
        """Add a new data object to a company"""
        return self.model.add_object(company_id, object_id, object_data)
    
    def add_new_user(self, user_id, name, role="standard"):
        """Add a new user to the system"""
        return self.model.add_user(user_id, name, role)
    
    def add_new_coi_class(self, coi_class_id, name):
        """Add a new conflict of interest class"""
        return self.model.add_coi_class(coi_class_id, name)
    
    def get_all_coi_classes(self):
        """Get all conflict of interest classes"""
        return self.model.coi_classes.keys()
    
    def get_all_companies(self):
        """Get all companies in the system"""
        return self.model.companies
    
    def get_all_users(self):
        """Get all users in the system"""
        return self.model.users
    
    def get_company_objects(self, company_id):
        """Get all objects for a specific company"""
        return self.model.get_company_objects(company_id)
    
    def simulate_access_attempt(self, user_id, company_id, object_id):
        """Simulate a user attempting to access a company's data"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.model.access_object(user_id, company_id, object_id, timestamp)
    
    def reset_user_history(self, user_id):
        """Reset a user's access history"""
        return self.model.reset_user_history(user_id)
