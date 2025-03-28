from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(50), unique=True, index=True)
    full_name = Column(String(100))
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(20))
    level = Column(String(20))  # Beginner, Intermediate, Advanced
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)
    enrollments = relationship("CourseEnrollment", back_populates="student")

class Teacher(Base):
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(20))
    specialization = Column(String(100))
    bio = Column(Text)
    active = Column(Boolean, default=True)
    courses = relationship("Course", back_populates="teacher")

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text)
    level = Column(String(20))
    max_students = Column(Integer)
    price = Column(Float)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    active = Column(Boolean, default=True)
    
    teacher = relationship("Teacher", back_populates="courses")
    enrollments = relationship("CourseEnrollment", back_populates="course")

class CourseEnrollment(Base):
    __tablename__ = "course_enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    payment_status = Column(String(20))  # Pending, Paid, Refunded
    
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
