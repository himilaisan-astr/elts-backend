from fastapi import APIRouter, Depends, HTTPException  
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter()


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
