from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Course as CourseModel
from schemas import CourseCreate, CourseUpdate, CourseOut, AnalysisResult
from services.conflict_detector import detect_conflicts
from services.optimizer import analyze_schedule

router = APIRouter(prefix="/api/courses", tags=["courses"])


def _get_or_404(course_id: int, db: Session) -> CourseModel:
    c = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Course not found")
    return c


@router.get("/", response_model=list[CourseOut])
def list_courses(db: Session = Depends(get_db)):
    return db.query(CourseModel).all()


@router.post("/", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(payload: CourseCreate, db: Session = Depends(get_db)):
    course = CourseModel(**payload.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@router.get("/{course_id}", response_model=CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    return _get_or_404(course_id, db)


@router.put("/{course_id}", response_model=CourseOut)
def update_course(
    course_id: int, payload: CourseUpdate, db: Session = Depends(get_db)
):
    course = _get_or_404(course_id, db)
    for field, value in payload.model_dump().items():
        setattr(course, field, value)
    db.commit()
    db.refresh(course)
    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = _get_or_404(course_id, db)
    db.delete(course)
    db.commit()


@router.get("/analyze/schedule", response_model=AnalysisResult)
def analyze(db: Session = Depends(get_db)):
    raw     = db.query(CourseModel).all()
    courses = [CourseOut.model_validate(c) for c in raw]
    conflicts          = detect_conflicts(courses)
    suggestions, score = analyze_schedule(courses)
    return AnalysisResult(conflicts=conflicts, suggestions=suggestions, score=score)
