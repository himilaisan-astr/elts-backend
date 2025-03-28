from fastapi import APIRouter, Depends, HTTPException  
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