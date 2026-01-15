"""Initialize database with sample users"""

from backend.database.database import SessionLocal, init_db, User
from backend.auth.security import get_password_hash
from datetime import datetime

def create_sample_users():
    """Create sample users for testing"""
    
    # Initialize database
    init_db()
    
    db = SessionLocal()
    
    # Check if users already exist
    existing_users = db.query(User).count()
    if existing_users > 0:
        print(f"⚠️  Database already contains {existing_users} users. Skipping sample data creation.")
        db.close()
        return
    
    # Sample users for each role
    sample_users = [
        {
            "username": "admin",
            "email": "admin@company.com",
            "full_name": "Admin User",
            "password": "admin123",
            "role": "admin",
            "department": "IT"
        },
        {
            "username": "john_finance",
            "email": "john@company.com",
            "full_name": "John Doe",
            "password": "finance123",
            "role": "finance",
            "department": "Finance"
        },
        {
            "username": "jane_marketing",
            "email": "jane@company.com",
            "full_name": "Jane Smith",
            "password": "marketing123",
            "role": "marketing",
            "department": "Marketing"
        },
        {
            "username": "bob_engineering",
            "email": "bob@company.com",
            "full_name": "Bob Johnson",
            "password": "engineering123",
            "role": "engineering",
            "department": "Engineering"
        },
        {
            "username": "alice_hr",
            "email": "alice@company.com",
            "full_name": "Alice Williams",
            "password": "hr123",
            "role": "hr",
            "department": "Human Resources"
        },
        {
            "username": "employee",
            "email": "employee@company.com",
            "full_name": "Regular Employee",
            "password": "employee123",
            "role": "employee",
            "department": "General"
        }
    ]
    
    print("Creating sample users...")
    
    for user_data in sample_users:
        password = user_data.pop("password")
        user = User(
            **user_data,
            hashed_password=get_password_hash(password),
            is_active=True,
            created_at=datetime.utcnow()
        )
        db.add(user)
        print(f"  ✓ Created user: {user.username} (role: {user.role})")
    
    db.commit()
    db.close()
    
    print(f"\n✅ Successfully created {len(sample_users)} sample users")
    print("\nSample login credentials:")
    print("=" * 60)
    for user_data in sample_users:
        # Reconstruct password from original data
        passwords = {
            "admin": "admin123",
            "john_finance": "finance123",
            "jane_marketing": "marketing123",
            "bob_engineering": "engineering123",
            "alice_hr": "hr123",
            "employee": "employee123"
        }
        print(f"Username: {user_data['username']:20} Password: {passwords.get(user_data['username'], 'N/A')}")
    print("=" * 60)


if __name__ == "__main__":
    create_sample_users()
