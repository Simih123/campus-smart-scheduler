import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from schemas import CourseOut, PriorityLevel
from services.optimizer import analyze_schedule


def make_course(id, name, days, start, end):
    return CourseOut(id=id, name=name, days=days,
                     start_time=start, end_time=end,
                     location="", priority=PriorityLevel.medium)


def test_empty_schedule_perfect_score():
    _, score = analyze_schedule([])
    assert score == 100

def test_late_evening_penalized():
    suggestions, score = analyze_schedule([make_course(1, "Night", "MWF", "20:00", "21:00")])
    assert any(s.category == "late_evening" for s in suggestions)
    assert score < 100

def test_large_gap_flagged():
    c1 = make_course(1, "Morning", "MWF", "08:00", "09:00")
    c2 = make_course(2, "Midday",  "MWF", "13:00", "14:00")
    suggestions, _ = analyze_schedule([c1, c2])
    assert any(s.category == "gap" for s in suggestions)

def test_small_gap_not_flagged():
    c1 = make_course(1, "First",  "MWF", "09:00", "10:00")
    c2 = make_course(2, "Second", "MWF", "10:15", "11:15")
    suggestions, _ = analyze_schedule([c1, c2])
    assert not any(s.category == "gap" for s in suggestions)

def test_heavy_day_flagged():
    courses = [make_course(i, f"C{i}", "M", f"{8+i}:00", f"{9+i}:00") for i in range(5)]
    suggestions, _ = analyze_schedule(courses)
    assert any(s.category == "workload" for s in suggestions)

def test_balanced_schedule_high_score():
    courses = [
        make_course(1, "Math",    "MWF", "09:00", "10:00"),
        make_course(2, "English", "TR",  "10:00", "11:00"),
    ]
    _, score = analyze_schedule(courses)
    assert score >= 80
