from fastapi import APIRouter, Depends, HTTPException  
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter()


# Student endpoints (No Admin Restriction)
@router.post("/students/", response_model=schemas.Student, tags=["Students"])
async def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.get("/students/", response_model=List[schemas.Student], tags=["Students"])
async def list_students(skip: int = 0, limit: int = 3000, db: Session = Depends(get_db)):
    return db.query(models.Student).offset(skip).limit(limit).all()

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

@router.delete("/students/bulk-delete", tags=["Students"])
async def bulk_delete_students(student_ids: List[int], db: Session = Depends(get_db)):
    db.query(models.Student).filter(models.Student.id.in_(student_ids)).delete(synchronize_session=False)
    db.commit()
    return {"message": f"{len(student_ids)} students deleted successfully"}

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