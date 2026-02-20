"""Role-Based Access Control Filtering"""

class RBACFilter:
    """Filter documents based on user roles"""
    
    def __init__(self):
        # Role hierarchy
        self.role_hierarchy = {
            "admin": ["admin", "finance", "engineering", "hr", "marketing", "employee"],
            "finance": ["finance", "employee"],
            "engineering": ["engineering", "employee"],
            "hr": ["hr", "employee"],
            "marketing": ["marketing", "employee"],
            "employee": ["employee"]
        }
    
    def can_access(self, user_role: str, required_roles: list) -> bool:
        """Check if user can access document with required roles"""
        if user_role not in self.role_hierarchy:
            return False
        
        user_roles = self.role_hierarchy[user_role]
        return any(role in user_roles for role in required_roles)
    
    def filter_results(self, results: list, user_role: str) -> list:
        """Filter search results based on user role"""
        filtered = []
        for result in results:
            allowed_roles = result.get("metadata", {}).get("allowed_roles", [])
            if self.can_access(user_role, allowed_roles):
                filtered.append(result)
        return filtered
