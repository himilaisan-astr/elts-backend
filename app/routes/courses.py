from fastapi import APIRouter, Depends, HTTPException  
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter()



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

@router.delete("/courses/bulk-delete", tags=["Courses"])
async def bulk_delete_courses(course_ids: List[int], db: Session = Depends(get_db)):
    db.query(models.Course).filter(models.Course.id.in_(course_ids)).delete(synchronize_session=False)
    db.commit()
    return {"message": f"{len(course_ids)} courses deleted successfully"}

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