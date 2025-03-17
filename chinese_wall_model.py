"""
Chinese Wall Model Implementation
This module contains the core logic for the Chinese Wall security model.
"""

from typing import Dict, List, Tuple, Any, Set, Optional

class ChineseWallModel:
    def __init__(self):
        # Dictionary to store conflict of interest classes
        # Format: {coi_class_id: {company_id: {object_id: object_data}}}
        self.coi_classes: Dict[str, Dict[str, Dict[str, str]]] = {}
        
        # Dictionary to track user access history
        # Format: {user_id: {company_id: True}}
        self.user_access_history: Dict[str, Dict[str, bool]] = {}
        
        # Dictionary to store access logs
        # Format: [{timestamp, user_id, company_id, object_id, access_granted}]
        self.access_logs: List[Dict[str, Any]] = []
        
        # Dictionary to store company information
        # Format: {company_id: {"name": name, "coi_class": coi_class_id}}
        self.companies: Dict[str, Dict[str, str]] = {}
        
        # Dictionary to store user information
        # Format: {user_id: {"name": name, "role": role}}
        self.users: Dict[str, Dict[str, str]] = {}
    
    def add_coi_class(self, coi_class_id: str, name: str) -> bool:
        """Add a new conflict of interest class"""
        if coi_class_id not in self.coi_classes:
            self.coi_classes[coi_class_id] = {}
            return True
        return False
    
    def add_company(self, company_id: str, name: str, coi_class_id: str) -> bool:
        """Add a new company to a conflict of interest class"""
        if coi_class_id not in self.coi_classes:
            return False
        
        if company_id not in self.coi_classes[coi_class_id]:
            self.coi_classes[coi_class_id][company_id] = {}
            self.companies[company_id] = {"name": name, "coi_class": coi_class_id}
            return True
        return False
    
    def add_object(self, company_id: str, object_id: str, object_data: str) -> bool:
        """Add a new object to a company dataset"""
        for coi_class_id, companies in self.coi_classes.items():
            if company_id in companies:
                self.coi_classes[coi_class_id][company_id][object_id] = object_data
                return True
        return False
    
    def add_user(self, user_id: str, name: str, role: str = "standard") -> bool:
        """Add a new user to the system"""
        if user_id not in self.users:
            self.users[user_id] = {"name": name, "role": role}
            self.user_access_history[user_id] = {}
            return True
        return False
    
    def can_access(self, user_id: str, company_id: str, object_id: Optional[str] = None) -> Tuple[bool, str]:
        """
        Check if a user can access a company's data based on Chinese Wall rules
        Returns: (bool, str) - (access_granted, reason)
        """
        # Check if user exists
        if user_id not in self.users:
            return False, "User does not exist"
        
        # Check if company exists
        if company_id not in self.companies:
            return False, "Company does not exist"
        
        # Get the COI class of the requested company
        requested_coi_class = self.companies[company_id]["coi_class"]
        
        # Check if user has accessed any company in the same COI class
        for accessed_company_id in self.user_access_history.get(user_id, {}):
            if accessed_company_id == company_id:
                # User has already accessed this company, so access is allowed
                return True, "Access granted - previously accessed company"
            
            accessed_company_coi_class = self.companies[accessed_company_id]["coi_class"]
            if accessed_company_coi_class == requested_coi_class and accessed_company_id != company_id:
                # User has accessed a different company in the same COI class
                return False, f"Access denied - conflict with previously accessed company: {self.companies[accessed_company_id]['name']}"
        
        # No conflicts found, access is allowed
        return True, "Access granted - no conflicts"
    
    def access_object(self, user_id: str, company_id: str, object_id: str, timestamp: str) -> Tuple[bool, str]:
        """
        Attempt to access an object and record the access
        Returns: (bool, str) - (access_granted, reason)
        """
        access_granted, reason = self.can_access(user_id, company_id)
        
        # Record the access attempt
        log_entry = {
            "timestamp": timestamp,
            "user_id": user_id,
            "user_name": self.users.get(user_id, {}).get("name", "Unknown"),
            "company_id": company_id,
            "company_name": self.companies.get(company_id, {}).get("name", "Unknown"),
            "object_id": object_id,
            "access_granted": access_granted,
            "reason": reason
        }
        self.access_logs.append(log_entry)
        
        # If access is granted, update the user's access history
        if access_granted:
            if user_id not in self.user_access_history:
                self.user_access_history[user_id] = {}
            self.user_access_history[user_id][company_id] = True
        
        return access_granted, reason
    
    def get_company_objects(self, company_id: str) -> Dict[str, str]:
        """Get all objects for a specific company"""
        for coi_class_id, companies in self.coi_classes.items():
            if company_id in companies:
                return companies[company_id]
        return {}
    
    def get_user_accessible_companies(self, user_id: str) -> List[str]:
        """Get all companies a user can access based on their history"""
        accessible_companies = []
        
        # If user has no access history, they can access any company
        if user_id not in self.user_access_history or not self.user_access_history[user_id]:
            return list(self.companies.keys())
        
        # Get the COI classes the user has already accessed
        accessed_coi_classes: Set[str] = set()
        for company_id in self.user_access_history[user_id]:
            accessed_coi_classes.add(self.companies[company_id]["coi_class"])
            # User can always access companies they've already accessed
            accessible_companies.append(company_id)
        
        # Add companies from COI classes the user hasn't accessed yet
        for company_id, company_info in self.companies.items():
            if company_info["coi_class"] not in accessed_coi_classes and company_id not in accessible_companies:
                accessible_companies.append(company_id)
        
        return accessible_companies
    
    def generate_report(self) -> List[Dict[str, Any]]:
        """Generate a report of all access logs"""
        return self.access_logs
    
    def reset_user_history(self, user_id: str) -> bool:
        """Reset a user's access history"""
        if user_id in self.user_access_history:
            self.user_access_history[user_id] = {}
            return True
        return False
    
    def get_coi_structure(self) -> List[Dict[str, Any]]:
        """Get the structure of COI classes and companies for visualization"""
        structure = []
        for coi_class_id in self.coi_classes:
            companies_in_class = []
            for company_id in self.coi_classes[coi_class_id]:
                companies_in_class.append({
                    "id": company_id,
                    "name": self.companies[company_id]["name"],
                    "objects": len(self.coi_classes[coi_class_id][company_id])
                })
            structure.append({
                "coi_class_id": coi_class_id,
                "companies": companies_in_class
            })
        return structure
