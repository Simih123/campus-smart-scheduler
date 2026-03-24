import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from schemas import CourseOut, PriorityLevel
from services.conflict_detector import detect_conflicts


def make_course(id, name, days, start, end):
    return CourseOut(id=id, name=name, days=days,
                     start_time=start, end_time=end,
                     location="", priority=PriorityLevel.medium)


def test_no_courses():
    assert detect_conflicts([]) == []

def test_single_course():
    assert detect_conflicts([make_course(1, "Math", "MWF", "09:00", "10:00")]) == []

def test_no_conflict_different_days():
    c1 = make_course(1, "Math",    "MWF", "09:00", "10:00")
    c2 = make_course(2, "English", "TR",  "09:00", "10:00")
    assert detect_conflicts([c1, c2]) == []

def test_no_conflict_adjacent_times():
    c1 = make_course(1, "Math",    "MWF", "09:00", "10:00")
    c2 = make_course(2, "Physics", "MWF", "10:00", "11:00")
    assert detect_conflicts([c1, c2]) == []

def test_conflict_full_overlap():
    c1 = make_course(1, "Math",    "MWF", "09:00", "10:00")
    c2 = make_course(2, "Physics", "MWF", "09:00", "10:00")
    assert len(detect_conflicts([c1, c2])) == 1

def test_conflict_partial_overlap():
    c1 = make_course(1, "Math",    "TR", "10:00", "11:30")
    c2 = make_course(2, "Physics", "TR", "11:00", "12:30")
    assert len(detect_conflicts([c1, c2])) == 1

def test_multiple_conflicts():
    c1 = make_course(1, "A", "MWF", "09:00", "10:00")
    c2 = make_course(2, "B", "MWF", "09:30", "10:30")
    c3 = make_course(3, "C", "MWF", "09:15", "09:45")
    assert len(detect_conflicts([c1, c2, c3])) == 3
