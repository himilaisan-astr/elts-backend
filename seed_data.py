from datetime import datetime, timedelta
import random
from faker import Faker
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Student, Teacher, Course, CourseEnrollment

# Initialize Faker
fake = Faker()

# Create database tables
Base.metadata.create_all(bind=engine)

def create_seed_data():
    db = SessionLocal()
    try:
        # Create teachers
        teachers = []
        specializations = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'History', 'Computer Science']
        for _ in range(20):
            teacher = Teacher(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone=fake.numerify(text='###-###-####'),
                specialization=random.choice(specializations),
                bio=fake.text(max_nb_chars=500),
                active=True
            )
            db.add(teacher)
            teachers.append(teacher)
        db.commit()

        # Create courses
        courses = []
        courses_data = [
            {
                'name': 'Advanced Mathematics',
                'description': 'Explore complex mathematical concepts including calculus, linear algebra, and differential equations. Perfect for students preparing for higher education in STEM fields.',
                'level': 'Advanced'
            },
            {
                'name': 'Physics 101',
                'description': 'Introduction to fundamental physics concepts including mechanics, energy, and waves. Includes hands-on experiments and practical applications.',
                'level': 'Beginner'
            },
            {
                'name': 'Chemistry Basics',
                'description': 'Learn the fundamentals of chemistry including atomic structure, chemical bonding, and reactions. Features interactive lab sessions and real-world applications.',
                'level': 'Beginner'
            },
            {
                'name': 'Biology Fundamentals',
                'description': 'Comprehensive introduction to biology covering cells, genetics, evolution, and ecosystems. Includes microscope work and field studies.',
                'level': 'Beginner'
            },
            {
                'name': 'English Literature',
                'description': 'Analysis of classic and contemporary literature, focusing on critical thinking and writing skills. Includes poetry, prose, and drama.',
                'level': 'Intermediate'
            },
            {
                'name': 'World History',
                'description': 'Journey through major historical events and civilizations from ancient times to modern day. Emphasis on cultural understanding and historical analysis.',
                'level': 'Intermediate'
            },
            {
                'name': 'Programming Basics',
                'description': 'Introduction to programming concepts using Python. Learn variables, control structures, functions, and basic algorithms.',
                'level': 'Beginner'
            },
            {
                'name': 'Data Structures',
                'description': 'Advanced programming course covering essential data structures and algorithms. Includes arrays, linked lists, trees, and graph algorithms.',
                'level': 'Advanced'
            },
            {
                'name': 'Web Development',
                'description': 'Learn modern web development using HTML, CSS, JavaScript, and popular frameworks. Build responsive and interactive websites.',
                'level': 'Intermediate'
            },
            {
                'name': 'Machine Learning',
                'description': 'Explore AI and machine learning concepts, algorithms, and applications. Includes practical projects using Python and popular ML libraries.',
                'level': 'Advanced'
            }
        ]
        
        for course_data in courses_data:
            start_date = datetime.now() + timedelta(days=random.randint(1, 30))
            course = Course(
                name=course_data['name'],
                description=course_data['description'],
                level=course_data['level'],
                max_students=random.randint(20, 30),
                price=random.uniform(500, 1500),
                start_date=start_date,
                end_date=start_date + timedelta(days=90),
                teacher_id=random.choice(teachers).id,
                active=True
            )
            db.add(course)
            courses.append(course)
        db.commit()

        # Create students
        levels = ['Beginner', 'Intermediate', 'Advanced']
        students = []
        for _ in range(150):
            student = Student(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone=fake.numerify(text='###-###-####'),
                level=random.choice(levels),
                enrollment_date=datetime.now() - timedelta(days=random.randint(0, 365)),
                active=True
            )
            db.add(student)
            students.append(student)
        db.commit()

        # Create enrollments (some students enrolled in multiple courses)
        payment_statuses = ['Pending', 'Paid', 'Refunded']
        for student in students:
            # Each student enrolls in 1-3 courses
            num_courses = random.randint(1, 3)
            selected_courses = random.sample(courses, num_courses)
            
            for course in selected_courses:
                enrollment = CourseEnrollment(
                    student_id=student.id,
                    course_id=course.id,
                    enrollment_date=datetime.now() - timedelta(days=random.randint(0, 90)),
                    payment_status=random.choice(payment_statuses)
                )
                db.add(enrollment)
        db.commit()

        print("Successfully created:")
        print(f"- {len(teachers)} teachers")
        print(f"- {len(courses)} courses")
        print(f"- {len(students)} students")
        print("Database seeded successfully!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_seed_data()
