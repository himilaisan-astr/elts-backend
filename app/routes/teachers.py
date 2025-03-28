from fastapi import APIRouter, Depends, HTTPException  
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter()


# Teacher endpoints (No Admin Restriction)
@router.post("/teachers/", response_model=schemas.Teacher, tags=["Teachers"])
async def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    db_teacher = models.Teacher(**teacher.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@router.get("/teachers/", response_model=List[schemas.Teacher], tags=["Teachers"])
async def list_teachers(skip: int = 0, limit: int = 500, db: Session = Depends(get_db)):
    return db.query(models.Teacher).offset(skip).limit(limit).all()

@router.put("/teachers/bulk-activate", tags=["Teachers"])
async def bulk_activate_teachers(teacher_ids: List[int], db: Session = Depends(get_db)):
    db.query(models.Teacher).filter(models.Teacher.id.in_(teacher_ids)).update({models.Teacher.active: True})
    db.commit()
    return {"message": f"{len(teacher_ids)} teachers activated successfully"}

@router.put("/teachers/bulk-deactivate", tags=["Teachers"])
async def bulk_deactivate_teachers(teacher_ids: List[int], db: Session = Depends(get_db)):
    db.query(models.Teacher).filter(models.Teacher.id.in_(teacher_ids)).update({models.Teacher.active: False})
    db.commit()
    return {"message": f"{len(teacher_ids)} teachers deactivated successfully"}

@router.delete("/teachers/bulk-delete", tags=["Teachers"])
async def bulk_delete_teachers(teacher_ids: List[int], db: Session = Depends(get_db)):
    db.query(models.Teacher).filter(models.Teacher.id.in_(teacher_ids)).delete(synchronize_session=False)
    db.commit()
    return {"message": f"{len(teacher_ids)} teachers deleted successfully"}

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
