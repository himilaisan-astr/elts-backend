import random
from datetime import datetime, timedelta
from faker import Faker
import requests
import json

# Initialize Faker with English locales
fake = Faker(['en_US', 'en_GB'])

# API endpoints
BASE_URL = "http://localhost:8000/api"
TEACHERS_URL = f"{BASE_URL}/teachers"
STUDENTS_URL = f"{BASE_URL}/students"
COURSES_URL = f"{BASE_URL}/courses"

# Teacher specializations
SPECIALIZATIONS = [
    "General English",
    "Business English",
    "IELTS Preparation",
    "TOEFL Preparation",
    "Academic Writing",
    "Conversation Skills"
]

# Teacher bios
TEACHER_BIO_TEMPLATES = [
    "Has {} years of experience teaching English. Specializes in {} with a focus on interactive learning.",
    "Certified {} instructor with {} years of teaching experience. Passionate about helping students achieve their language goals.",
    "Experienced {} teacher with a {} degree in Education. Has taught students from diverse backgrounds for {} years.",
    "Dedicated English teacher specializing in {}. {} years of experience in both group and individual instruction."
]

def generate_teacher_bio(specialization):
    years = random.randint(5, 20)
    degree = random.choice(["Master's", "Bachelor's", "TESOL", "CELTA"])
    return random.choice(TEACHER_BIO_TEMPLATES).format(years, specialization, degree, years)

def generate_teachers(count=20):
    teachers = []
    # Use only English-speaking locales for teachers
    teacher_fake = Faker(['en_US', 'en_GB', 'en_AU', 'en_CA'])
    
    for _ in range(count):
        first_name = teacher_fake.first_name()
        last_name = teacher_fake.last_name()
        specialization = random.choice(SPECIALIZATIONS)
        
        teacher = {
            "first_name": first_name,
            "last_name": last_name,
            "email": f"{first_name.lower()}.{last_name.lower()}@elts.edu",
            "phone": teacher_fake.phone_number(),
            "specialization": specialization,
            "bio": generate_teacher_bio(specialization),
            "active": True
        }
        teachers.append(teacher)
    return teachers

def generate_students(count=100):
    students = []
    levels = ["Beginner"] * 40 + ["Intermediate"] * 40 + ["Advanced"] * 20
    random.shuffle(levels)
    
    for i in range(count):
        first_name = fake.first_name()
        last_name = fake.last_name()
        enrollment_date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
        
        student = {
            "first_name": first_name,
            "last_name": last_name,
            "email": f"{first_name.lower()}.{last_name.lower()}{random.randint(1,999)}@gmail.com",
            "phone": f"+{random.randint(1,99)}{fake.msisdn()[3:]}",
            "level": levels[i],
            "enrollment_date": enrollment_date,
            "active": random.random() < 0.9  # 90% active
        }
        students.append(student)
    return students

def generate_courses(teachers):
    courses = [
        {
            "name": "Foundation English",
            "description": "A comprehensive course designed for beginners to build a strong foundation in English. Covers basic grammar, vocabulary, and essential communication skills.",
            "level": "Beginner",
            "max_students": 20,
            "price": 300.0,
            "start_date": (datetime.now() + timedelta(days=random.randint(7, 30))).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=random.randint(90, 120))).strftime("%Y-%m-%d"),
            "active": True
        },
        {
            "name": "English for Business",
            "description": "Master business English communication skills. Focus on professional vocabulary, email writing, presentations, and negotiation skills.",
            "level": "Intermediate",
            "max_students": 15,
            "price": 500.0,
            "start_date": (datetime.now() + timedelta(days=random.randint(7, 30))).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=random.randint(60, 90))).strftime("%Y-%m-%d"),
            "active": True
        },
        {
            "name": "IELTS Preparation",
            "description": "Intensive IELTS preparation course covering all four modules: Reading, Writing, Listening, and Speaking. Includes practice tests and personalized feedback.",
            "level": "Advanced",
            "max_students": 15,
            "price": 800.0,
            "start_date": (datetime.now() + timedelta(days=random.randint(7, 30))).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=random.randint(90, 120))).strftime("%Y-%m-%d"),
            "active": True
        },
        {
            "name": "Conversational English",
            "description": "Improve your speaking and listening skills through interactive sessions. Focus on pronunciation, fluency, and natural conversation.",
            "level": "Intermediate",
            "max_students": 18,
            "price": 400.0,
            "start_date": (datetime.now() + timedelta(days=random.randint(7, 30))).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=random.randint(60, 90))).strftime("%Y-%m-%d"),
            "active": True
        },
        {
            "name": "Academic Writing",
            "description": "Learn to write academic essays, research papers, and dissertations. Covers academic vocabulary, citation styles, and research methodology.",
            "level": "Advanced",
            "max_students": 15,
            "price": 600.0,
            "start_date": (datetime.now() + timedelta(days=random.randint(7, 30))).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=random.randint(60, 90))).strftime("%Y-%m-%d"),
            "active": True
        }
    ]
    
    # Assign teachers based on specialization
    for course in courses:
        suitable_teachers = [t for t in teachers if t["specialization"] in course["name"] or 
                           (t["specialization"] == "General English" and course["level"] == "Beginner")]
        if not suitable_teachers:
            suitable_teachers = teachers  # Fallback to any teacher
        selected_teacher = random.choice(suitable_teachers)
        course["teacher_id"] = selected_teacher["id"]
    
    return courses

def populate_data():
    print("Generating and inserting teachers...")
    teachers = generate_teachers()
    created_teachers = []
    for teacher in teachers:
        response = requests.post(TEACHERS_URL, json=teacher)
        if response.status_code == 200:
            created_teacher = response.json()
            print(f"Created teacher: {created_teacher['first_name']} {created_teacher['last_name']}")
            created_teachers.append(created_teacher)
        else:
            print(f"Failed to create teacher: {response.status_code} - {response.text}")
    
    print("\nGenerating and inserting students...")
    students = generate_students()
    for student in students:
        response = requests.post(STUDENTS_URL, json=student)
        if response.status_code == 200:
            print(f"Created student: {student['first_name']} {student['last_name']}")
        else:
            print(f"Failed to create student: {response.status_code} - {response.text}")
    
    print("\nGenerating and inserting courses...")
    courses = generate_courses(created_teachers)
    for course in courses:
        response = requests.post(COURSES_URL, json=course)
        if response.status_code == 200:
            print(f"Created course: {course['name']}")
        else:
            print(f"Failed to create course: {response.status_code} - {response.text}")

if __name__ == "__main__":
    print("Starting data population...")
    populate_data()
    print("\nData population completed!")
