from datetime import date, datetime, timedelta
from typing import Any


def generate_slots(
    target_date: date,
    schedules: list,
    slot_duration: int,
    booked_slots: list,
    exceptions: list | None = None,
) -> list[dict[str, Any]]:
    """
    Returns a list of {start_time, end_time, available} slots for a given date,
    considering schedules, exceptions, and already booked appointments.
    """
    exceptions = exceptions or []

    active_schedules = schedules
    for exc in exceptions:
        if exc.exception_date == target_date:
            if exc.is_closed:
                return []
            active_schedules = [
                type("S", (), {"start_time": exc.open_time, "end_time": exc.close_time})()
            ]
            break

    booked_times = {
        (a.start_time.strftime("%H:%M:%S"), a.end_time.strftime("%H:%M:%S"))
        for a in booked_slots
        if a.status not in ("cancelled",)
    }

    slots: list[dict[str, Any]] = []
    delta = timedelta(minutes=slot_duration)

    for schedule in active_schedules:
        current = datetime.combine(target_date, schedule.start_time)
        end = datetime.combine(target_date, schedule.end_time)

        while current + delta <= end:
            slot_start = current.time().strftime("%H:%M:%S")
            slot_end = (current + delta).time().strftime("%H:%M:%S")
            available = (slot_start, slot_end) not in booked_times
            slots.append(
                {
                    "start_time": slot_start,
                    "end_time": slot_end,
                    "available": available,
                }
            )
            current += delta

    return slots
