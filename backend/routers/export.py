from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from database import get_db
from models import Course as CourseModel
from schemas import CourseOut
from services.ics_exporter import build_ics

router = APIRouter(prefix="/api/export", tags=["export"])


@router.get("/ics")
def export_ics(db: Session = Depends(get_db)):
    raw = db.query(CourseModel).all()
    courses = [CourseOut.model_validate(c) for c in raw]
    ics_bytes = build_ics(courses)
    return Response(
        content=ics_bytes,
        media_type="text/calendar",
        headers={"Content-Disposition": 'attachment; filename="schedule.ics"'},
    )
