import random
from datetime import datetime, timedelta
from faker import Faker
import requests
import json
from collections import defaultdict

# Initialize Faker with English locales
fake = Faker(['en_US', 'en_GB'])

# API endpoints
BASE_URL = "http://localhost:8000/api"
TEACHERS_URL = f"{BASE_URL}/teachers"
STUDENTS_URL = f"{BASE_URL}/students"
COURSES_URL = f"{BASE_URL}/courses"
ENROLLMENTS_URL = f"{BASE_URL}/enrollments"

# Teacher specializations
SPECIALIZATIONS = [
    "General English",
    "Business English",
    "IELTS Preparation",
    "TOEFL Preparation",
    "Academic Writing",
    "Conversation Skills",
    "Grammar & Vocabulary",
    "English for Young Learners",
    "English for Specific Purposes",
    "Advanced Grammar",
    "English for Professionals",
    "English for Travel",
    "Pronunciation and Fluency",
    "English for Media and Journalism",
    "Creative Writing in English",
    "English for Tech Industry",
    "Legal English",
    "Medical English",
    "English for Hospitality"
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

def generate_teachers(count=200):
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

def generate_students(count=2000):
    students = []
    levels = ["Beginner"] * 800 + ["Intermediate"] * 800 + ["Advanced"] * 400
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
            "max_students": 30,
            "price": 300.0,
            "start_date": (datetime.now() + timedelta(days=random.randint(7, 30))).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=random.randint(90, 120))).strftime("%Y-%m-%d"),
            "active": True
        },
        {
            "name": "English for Business",
            "description": "Master business English communication skills. Focus on professional vocabulary, email writing, presentations, and negotiation skills.",
            "level": "Intermediate",
            "max_students": 20,
            "price": 500.0,
            "start_date": (datetime.now() + timedelta(days=random.randint(7, 30))).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=random.randint(60, 90))).strftime("%Y-%m-%d"),
            "active": True
        },
        {
            "name": "IELTS Preparation",
            "description": "Intensive IELTS preparation course covering all four modules: Reading, Writing, Listening, and Speaking. Includes practice tests and personalized feedback.",
            "level": "Advanced",
            "max_students": 20,
            "price": 800.0,
            "start_date": (datetime.now() + timedelta(days=random.randint(7, 30))).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=random.randint(90, 120))).strftime("%Y-%m-%d"),
            "active": True
        },
        {
            "name": "Conversational English",
            "description": "Improve your speaking and listening skills through interactive sessions. Focus on pronunciation, fluency, and natural conversation.",
            "level": "Intermediate",
            "max_students": 25,
            "price": 400.0,
            "start_date": (datetime.now() + timedelta(days=random.randint(7, 30))).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=random.randint(60, 90))).strftime("%Y-%m-%d"),
            "active": True
        },
        {
            "name": "Academic Writing",
            "description": "Learn to write academic essays, research papers, and dissertations. Covers academic vocabulary, citation styles, and research methodology.",
            "level": "Advanced",
            "max_students": 20,
            "price": 600.0,
            "start_date": (datetime.now() + timedelta(days=random.randint(7, 30))).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=random.randint(60, 90))).strftime("%Y-%m-%d"),
            "active": True
        },
        {
            "name": "English Grammar Mastery",
            "description": "In-depth grammar course covering tenses, sentence structures, and complex grammatical rules for all levels.",
            "level": "Intermediate",
            "max_students": 30,
            "price": 350.0,
            "start_date": (datetime.now() + timedelta(days=random.randint(7, 30))).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=random.randint(60, 90))).strftime("%Y-%m-%d"),
            "active": True
        },
        {
            "name": "English for Young Learners",
            "description": "Engaging and fun course for young learners focusing on basic English skills through games, songs, and interactive activities.",
            "level": "Beginner",
            "max_students": 40,
            "price": 250.0,
            "start_date": (datetime.now() + timedelta(days=random.randint(7, 30))).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=random.randint(90, 120))).strftime("%Y-%m-%d"),
            "active": True
        },
        {
            "name": "TOEFL Preparation",
            "description": "Prepare for the TOEFL exam with practice tests, strategies, and guidance on improving your score across all sections.",
            "level": "Advanced",
            "max_students": 20,
            "price": 750.0,
            "start_date": (datetime.now() + timedelta(days=random.randint(7, 30))).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=random.randint(90, 120))).strftime("%Y-%m-%d"),
            "active": True
        },
        {
            "name": "English for Specific Purposes (ESP)",
            "description": "Learn English tailored for your profession or academic field, including medical, legal, and technical English.",
            "level": "Intermediate",
            "max_students": 20,
            "price": 550.0,
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

def calculate_monthly_revenue(courses):
    monthly_revenue = defaultdict(float)
    
    for course in courses:
        start_date = datetime.strptime(course['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(course['end_date'], '%Y-%m-%d')
        
        # Calculate course duration in months
        duration_days = (end_date - start_date).days
        duration_months = duration_days / 30  # Approximate months
        
        # Calculate monthly revenue for this course
        monthly_course_revenue = course['price'] / duration_months
        
        # Add revenue to each month the course runs
        current_date = start_date
        while current_date <= end_date:
            month_key = current_date.strftime('%Y-%m')
            monthly_revenue[month_key] += monthly_course_revenue
            # Move to next month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
    
    return monthly_revenue

def generate_enrollments(courses, num_enrollments=500):
    # Get all students and courses
    students_response = requests.get(STUDENTS_URL)
    if students_response.status_code != 200:
        print("Failed to fetch students")
        return []
    students = students_response.json()

    enrollments = []
    for _ in range(num_enrollments):
        student = random.choice(students)
        course = random.choice(courses)
        
        # Generate a random enrollment date between course creation and start date
        start_date = datetime.fromisoformat(course['start_date'].replace('Z', '+00:00'))
        enrollment_date = (start_date - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
        
        enrollment = {
            "student_id": student['id'],
            "course_id": course['id'],
            "enrollment_date": enrollment_date,
            "payment_status": random.choice(["Paid"] * 9 + ["Pending"]),  # 90% paid
            "active": True
        }
        enrollments.append(enrollment)
    
    return enrollments

def populate_data():
    print("Generating and inserting teachers...")
    teachers = generate_teachers(200)
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
    students = generate_students(2000)
    created_students = []
    for student in students:
        response = requests.post(STUDENTS_URL, json=student)
        if response.status_code == 200:
            created_student = response.json()
            print(f"Created student: {student['first_name']} {student['last_name']}")
            created_students.append(created_student)
        else:
            print(f"Failed to create student: {response.status_code} - {response.text}")
    
    print("\nGenerating and inserting courses...")
    courses = generate_courses(created_teachers)
    created_courses = []
    for course in courses:
        response = requests.post(COURSES_URL, json=course)
        if response.status_code == 200:
            created_course = response.json()
            print(f"Created course: {course['name']}")
            created_courses.append(created_course)
        else:
            print(f"Failed to create course: {response.status_code} - {response.text}")
    
    print("\nGenerating and inserting enrollments...")
    enrollments = generate_enrollments(created_courses)
    for enrollment in enrollments:
        response = requests.post(ENROLLMENTS_URL, json=enrollment)
        if response.status_code == 200:
            print(f"Created enrollment for student {enrollment['student_id']} in course {enrollment['course_id']}")
        else:
            print(f"Failed to create enrollment: {response.status_code} - {response.text}")
    
    print("\nCalculating monthly revenue...")
    monthly_revenue = calculate_monthly_revenue(courses)
    for month, revenue in sorted(monthly_revenue.items()):
        print(f"Month {month}: ${revenue:.2f}")

if __name__ == "__main__":
    print("Starting data population...")
    populate_data()
    print("\nData population completed!")
