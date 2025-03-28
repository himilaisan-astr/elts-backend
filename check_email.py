from app.database import SessionLocal
from app.models import User

def check_email(email: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            print(f"Email {email} is already registered")
        else:
            print(f"Email {email} is not registered")
    except Exception as e:
        print(f"Error checking email: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_email("vinh.nguyen@eltschool.co.uk")
