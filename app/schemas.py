from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Student Schemas
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    level: str

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    enrollment_date: datetime
    active: bool

    class Config:
        from_attributes = True

# Teacher Schemas
class TeacherBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    specialization: str
    bio: str

class TeacherCreate(TeacherBase):
    pass

class Teacher(TeacherBase):
    id: int
    active: bool

    class Config:
        from_attributes = True

# Course Schemas
class CourseBase(BaseModel):
    name: str
    description: str
    level: str
    max_students: int
    price: float
    start_date: datetime
    end_date: datetime
    teacher_id: int

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    active: bool

    class Config:
        from_attributes = True

# CourseEnrollment Schemas
class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    payment_status: str = "Pending"

class EnrollmentCreate(EnrollmentBase):
    pass

class Enrollment(EnrollmentBase):
    id: int
    enrollment_date: datetime

    class Config:
        from_attributes = True

# Response Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class DashboardStats(BaseModel):
    total_students: int
    total_teachers: int
    total_courses: int
    active_enrollments: int
    revenue_this_month: float
