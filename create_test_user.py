from app.database import SessionLocal, engine, Base
from app.models import User
from app.security import get_password_hash

def create_test_user():
    db = SessionLocal()
    try:
        # Check if test user already exists
        test_user = db.query(User).filter(User.email == "test@test.com").first()
        if not test_user:
            # Create test user
            test_user = User(
                email="test@test.com",
                username="test",
                full_name="Test User",
                hashed_password=get_password_hash("test123"),
                is_active=True,
                is_admin=True
            )
            db.add(test_user)
            db.commit()
            print("Test user created successfully!")
            print("Email: test@test.com")
            print("Password: test123")
        else:
            print("Test user already exists!")
            print("Email: test@test.com")
            print("Password: test123")
    except Exception as e:
        print(f"Error creating test user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    create_test_user()
