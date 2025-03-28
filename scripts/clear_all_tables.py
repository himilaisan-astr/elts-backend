import sys, os
from sqlalchemy import text

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.database import engine

def clear_all_tables():
    with engine.connect() as conn:
        with conn.begin():
            # Delete in order of dependencies
            tables = ['course_enrollments', 'courses', 'students', 'teachers']
            for table in tables:
                print(f"Deleting {table}...")
                conn.execute(text(f"DELETE FROM {table}"))
            print("All tables cleared successfully!")

if __name__ == "__main__":
    try:
        clear_all_tables()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
