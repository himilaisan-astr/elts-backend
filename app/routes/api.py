from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter()

# Dashboard Statistics (No Admin Restriction)
@router.get("/dashboard/stats/", response_model=schemas.DashboardStats, tags=["Dashboard"])
async def get_dashboard_stats(db: Session = Depends(get_db)):
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

# Student endpoints (No Admin Restriction)
@router.post("/students/", response_model=schemas.Student, tags=["Students"])
async def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.get("/students/", response_model=List[schemas.Student], tags=["Students"])
async def list_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Student).offset(skip).limit(limit).all()

@router.delete("/students/{student_id}", tags=["Students"])
async def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}

@router.put("/students/{student_id}/activate", tags=["Students"])
async def activate_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.active = True
    db.commit()
    return {"message": "Student activated successfully"}

@router.put("/students/{student_id}/deactivate", tags=["Students"])
async def deactivate_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.active = False
    db.commit()
    return {"message": "Student deactivated successfully"}

@router.put("/students/bulk-activate", tags=["Students"])
async def bulk_activate_students(student_ids: List[int], db: Session = Depends(get_db)):
    db.query(models.Student).filter(models.Student.id.in_(student_ids)).update({models.Student.active: True})
    db.commit()
    return {"message": f"{len(student_ids)} students activated successfully"}

@router.put("/students/bulk-deactivate", tags=["Students"])
async def bulk_deactivate_students(student_ids: List[int], db: Session = Depends(get_db)):
    db.query(models.Student).filter(models.Student.id.in_(student_ids)).update({models.Student.active: False})
    db.commit()
    return {"message": f"{len(student_ids)} students deactivated successfully"}

# Teacher endpoints (No Admin Restriction)
@router.post("/teachers/", response_model=schemas.Teacher, tags=["Teachers"])
async def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    db_teacher = models.Teacher(**teacher.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@router.get("/teachers/", response_model=List[schemas.Teacher], tags=["Teachers"])
async def list_teachers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Teacher).offset(skip).limit(limit).all()

@router.delete("/teachers/{teacher_id}", tags=["Teachers"])
async def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    db.delete(teacher)
    db.commit()
    return {"message": "Teacher deleted successfully"}

@router.put("/teachers/{teacher_id}/activate", tags=["Teachers"])
async def activate_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    teacher.active = True
    db.commit()
    return {"message": "Teacher activated successfully"}

@router.put("/teachers/{teacher_id}/deactivate", tags=["Teachers"])
async def deactivate_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    teacher.active = False
    db.commit()
    return {"message": "Teacher deactivated successfully"}

@router.put("/teachers/bulk-activate", tags=["Teachers"])
async def bulk_activate_teachers(teacher_ids: List[int], db: Session = Depends(get_db), tags=["Teachers"]):
    db.query(models.Teacher).filter(models.Teacher.id.in_(teacher_ids)).update({models.Teacher.active: True})
    db.commit()
    return {"message": f"{len(teacher_ids)} teachers activated successfully"}

@router.put("/teachers/bulk-deactivate", tags=["Teachers"])
async def bulk_deactivate_teachers(teacher_ids: List[int], db: Session = Depends(get_db)):
    db.query(models.Teacher).filter(models.Teacher.id.in_(teacher_ids)).update({models.Teacher.active: False})
    db.commit()
    return {"message": f"{len(teacher_ids)} teachers deactivated successfully"}

# Course endpoints (No Admin Restriction)
@router.post("/courses/", response_model=schemas.Course, tags=["Courses"])
async def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db), tags=["Courses"]):
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/courses/", response_model=List[schemas.Course], tags=["Courses"])
async def list_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Course).offset(skip).limit(limit).all()

@router.get("/courses/{course_id}/students", response_model=List[schemas.Student], tags=["Courses"])
async def get_course_students(course_id: int, db: Session = Depends(get_db)):
    # Check if course exists
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Get all enrollments for this course and join with students
    students = db.query(models.Student)\
        .join(models.CourseEnrollment, models.Student.id == models.CourseEnrollment.student_id)\
        .filter(models.CourseEnrollment.course_id == course_id)\
        .all()
    
    return students

@router.delete("/courses/{course_id}", tags=["Courses"])
async def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}

@router.put("/courses/{course_id}/activate", tags=["Courses"])
async def activate_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    course.active = True
    db.commit()
    return {"message": "Course activated successfully"}

@router.put("/courses/{course_id}/deactivate", tags=["Courses"])
async def deactivate_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    course.active = False
    db.commit()
    return {"message": "Course deactivated successfully"}

@router.put("/courses/bulk-activate", tags=["Courses"])
async def bulk_activate_courses(course_ids: List[int], db: Session = Depends(get_db)):
    db.query(models.Course).filter(models.Course.id.in_(course_ids)).update({models.Course.active: True})
    db.commit()
    return {"message": f"{len(course_ids)} courses activated successfully"}

@router.put("/courses/bulk-deactivate", tags=["Courses"])
async def bulk_deactivate_courses(course_ids: List[int], db: Session = Depends(get_db)):
    db.query(models.Course).filter(models.Course.id.in_(course_ids)).update({models.Course.active: False})
    db.commit()
    return {"message": f"{len(course_ids)} courses deactivated successfully"}

# Enrollment endpoints (No Admin Restriction)
@router.post("/enrollments/", response_model=schemas.Enrollment, tags=["Enrollments"])
async def create_enrollment(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    # Check if course exists
    course = db.query(models.Course).filter(models.Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check if course is full
    current_enrollments = db.query(func.count(models.CourseEnrollment.id))\
        .filter(models.CourseEnrollment.course_id == enrollment.course_id).scalar()
    
    if current_enrollments >= course.max_students:
        raise HTTPException(status_code=400, detail="Course is full")
    
    db_enrollment = models.CourseEnrollment(**enrollment.dict())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

@router.get("/enrollments/", response_model=List[schemas.Enrollment], tags=["Enrollments"])
async def list_enrollments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), tags=["Enrollments"]):
    return db.query(models.CourseEnrollment).offset(skip).limit(limit).all()
