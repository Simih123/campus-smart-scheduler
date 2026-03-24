from pydantic import BaseModel, field_validator, model_validator
from enum import Enum
from typing import Optional
import re

class PriorityLevel(str, Enum):
    low    = "low"
    medium = "medium"
    high   = "high"

TIME_RE = re.compile(r"^\d{2}:\d{2}$")

class CourseBase(BaseModel):
    name:       str
    days:       str
    start_time: str
    end_time:   str
    location:   Optional[str] = ""
    priority:   PriorityLevel = PriorityLevel.medium

    @field_validator("days")
    @classmethod
    def validate_days(cls, v: str) -> str:
        allowed = set("MTWRFSUmtwrfsu")
        if not v or not all(c in allowed for c in v):
            raise ValueError("days must contain only M T W R F S U characters")
        return v.upper()

    @field_validator("start_time", "end_time")
    @classmethod
    def validate_time(cls, v: str) -> str:
        if not TIME_RE.match(v):
            raise ValueError("time must be in HH:MM format")
        h, m = int(v[:2]), int(v[3:])
        if not (0 <= h <= 23 and 0 <= m <= 59):
            raise ValueError("invalid time value")
        return v

    @model_validator(mode="after")
    def end_after_start(self) -> "CourseBase":
        if self.start_time >= self.end_time:
            raise ValueError("end_time must be after start_time")
        return self

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name must not be empty")
        return v.strip()

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class CourseOut(CourseBase):
    id: int
    model_config = {"from_attributes": True}

class ConflictDetail(BaseModel):
    course_a:     CourseOut
    course_b:     CourseOut
    overlap_days: str

class OptimizationSuggestion(BaseModel):
    category: str
    message:  str
    severity: str

class AnalysisResult(BaseModel):
    conflicts:   list[ConflictDetail]
    suggestions: list[OptimizationSuggestion]
    score:       int
