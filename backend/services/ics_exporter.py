from datetime import date, datetime, timedelta
from icalendar import Calendar, Event, vText, vDatetime
from schemas import CourseOut

DAY_TO_WEEKDAY = {"M": 0, "T": 1, "W": 2, "R": 3, "F": 4, "S": 5, "U": 6}
SEMESTER_START = date(2025, 8, 25)
WEEKS          = 16


def _next_weekday(start: date, weekday: int) -> date:
    days_ahead = (weekday - start.weekday()) % 7
    return start + timedelta(days=days_ahead)


def build_ics(courses: list[CourseOut]) -> bytes:
    cal = Calendar()
    cal.add("prodid", "-//Campus Smart Scheduler//EN")
    cal.add("version", "2.0")
    cal.add("calscale", "GREGORIAN")

    for course in courses:
        for day_char in course.days:
            weekday = DAY_TO_WEEKDAY.get(day_char)
            if weekday is None:
                continue
            first_day = _next_weekday(SEMESTER_START, weekday)
            for week in range(WEEKS):
                event_date = first_day + timedelta(weeks=week)
                sh, sm = map(int, course.start_time.split(":"))
                eh, em = map(int, course.end_time.split(":"))
                event = Event()
                event.add("summary",     vText(course.name))
                event.add("dtstart",     vDatetime(datetime(event_date.year, event_date.month, event_date.day, sh, sm)))
                event.add("dtend",       vDatetime(datetime(event_date.year, event_date.month, event_date.day, eh, em)))
                event.add("location",    vText(course.location or ""))
                event.add("description", vText(f"Priority: {course.priority}"))
                cal.add_component(event)

    return cal.to_ical()
