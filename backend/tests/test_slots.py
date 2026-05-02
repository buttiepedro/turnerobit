from datetime import date, time

import pytest

from app.utils.slot_generator import generate_slots


class _Schedule:
    def __init__(self, start, end):
        self.start_time = start
        self.end_time = end


class _Booked:
    def __init__(self, start, end, status="confirmed"):
        self.start_time = start
        self.end_time = end
        self.status = status


def test_generate_slots_basic():
    schedules = [_Schedule(time(9, 0), time(11, 0))]
    slots = generate_slots(date.today(), schedules, 30, [])
    assert len(slots) == 4
    assert all(s["available"] for s in slots)
    assert slots[0]["start_time"] == "09:00:00"
    assert slots[-1]["start_time"] == "10:30:00"


def test_booked_slot_is_unavailable():
    schedules = [_Schedule(time(9, 0), time(11, 0))]
    booked = [_Booked(time(9, 0), time(9, 30))]
    slots = generate_slots(date.today(), schedules, 30, booked)
    assert not slots[0]["available"]
    assert all(s["available"] for s in slots[1:])


def test_cancelled_slot_is_available():
    schedules = [_Schedule(time(9, 0), time(10, 0))]
    booked = [_Booked(time(9, 0), time(9, 30), status="cancelled")]
    slots = generate_slots(date.today(), schedules, 30, booked)
    assert all(s["available"] for s in slots)


def test_closed_exception_returns_empty():
    schedules = [_Schedule(time(9, 0), time(11, 0))]

    class _Exc:
        exception_date = date.today()
        is_closed = True
        open_time = None
        close_time = None

    slots = generate_slots(date.today(), schedules, 30, [], [_Exc()])
    assert slots == []
