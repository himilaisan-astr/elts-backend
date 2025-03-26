from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter()

# Dashboard Statistics
@router.get("/dashboard/stats/", response_model=schemas.DashboardStats)
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    total_students = db.query(func.count(models.Student.id)).scalar()
    total_teachers = db.query(func.count(models.Teacher.id)).scalar()
    total_courses = db.query(func.count(models.Course.id)).scalar()
    active_enrollments = db.query(func.count(models.CourseEnrollment.id))\
        .filter(models.CourseEnrollment.payment_status == "Paid").scalar()
    
    # Calculate revenue for current month
    current_month = datetime.utcnow().replace(day=1)
    revenue = db.query(func.sum(models.Course.price))\
        .join(models.CourseEnrollment)\
        .filter(
            models.CourseEnrollment.payment_status == "Paid",
            models.CourseEnrollment.enrollment_date >= current_month
        ).scalar() or 0.0

    return {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_courses": total_courses,
        "active_enrollments": active_enrollments,
        "revenue_this_month": revenue
    }

# Student endpoints
@router.post("/students/", response_model=schemas.Student)
async def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.get("/students/", response_model=List[schemas.Student])
async def list_students(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    students = db.query(models.Student).offset(skip).limit(limit).all()
    return students

# Teacher endpoints
@router.post("/teachers/", response_model=schemas.Teacher)
async def create_teacher(
    teacher: schemas.TeacherCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    db_teacher = models.Teacher(**teacher.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@router.get("/teachers/", response_model=List[schemas.Teacher])
async def list_teachers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    teachers = db.query(models.Teacher).offset(skip).limit(limit).all()
    return teachers

# Course endpoints
@router.post("/courses/", response_model=schemas.Course)
async def create_course(
    course: schemas.CourseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/courses/", response_model=List[schemas.Course])
async def list_courses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    courses = db.query(models.Course).offset(skip).limit(limit).all()
    return courses

# Enrollment endpoints
@router.post("/enrollments/", response_model=schemas.Enrollment)
async def create_enrollment(
    enrollment: schemas.EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    # Check if course has space
    course = db.query(models.Course).filter(models.Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    current_enrollments = db.query(func.count(models.CourseEnrollment.id))\
        .filter(models.CourseEnrollment.course_id == enrollment.course_id).scalar()
    
    if current_enrollments >= course.max_students:
        raise HTTPException(status_code=400, detail="Course is full")
    
    db_enrollment = models.CourseEnrollment(**enrollment.dict())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

@router.get("/enrollments/", response_model=List[schemas.Enrollment])
async def list_enrollments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    enrollments = db.query(models.CourseEnrollment).offset(skip).limit(limit).all()
    return enrollments
