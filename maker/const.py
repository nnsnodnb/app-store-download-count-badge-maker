import calendar
from datetime import datetime, timedelta
from enum import StrEnum
from typing import Optional


class Frequency(StrEnum):
    YEARLY = "YEARLY"
    MONTHLY = "MONTHLY"
    WEEKLY = "WEEKLY"
    DAILY = "DAILY"

    @property
    def badge_value(self) -> str:
        if self == Frequency.YEARLY:
            return "year"
        elif self == Frequency.MONTHLY:
            return "month"
        elif self == Frequency.WEEKLY:
            return "week"
        elif self == Frequency.DAILY:
            return "day"
        else:
            raise ValueError(f"Invalid frequency: {self}")

    def report_date(self) -> Optional[str]:
        base = datetime.now() - timedelta(days=2)
        if self == Frequency.YEARLY:
            return str(base.year - 1)
        elif self == Frequency.MONTHLY:
            base -= timedelta(days=base.day)
            return base.strftime("%Y-%m")
        elif self == Frequency.WEEKLY:
            # Specify the Sunday at the end of the week
            weekday = base.weekday()
            if weekday == calendar.SUNDAY:
                return base.strftime("%Y-%m-%d")
            else:
                base -= timedelta(days=weekday + 1)
                return base.strftime("%Y-%m-%d")
        elif self == Frequency.DAILY:
            return base.strftime("%Y-%m-%d")
        else:
            raise ValueError(f"Invalid frequency: {self}")


class Color(StrEnum):
    RED = "red"
    YELLOW = "yellow"
    YELLOWGREEN = "yellowgreen"
    GREEN = "green"
    BRIGHTGREEN = "brightgreen"
