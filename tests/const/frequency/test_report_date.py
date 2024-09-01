from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from maker.const import Frequency

utc = ZoneInfo("UTC")


@pytest.mark.parametrize(
    "today, frequency, expected",
    [
        (datetime(2024, 1, 2, tzinfo=utc), Frequency.YEARLY, "2022"),
        (datetime(2024, 1, 3, tzinfo=utc), Frequency.YEARLY, "2023"),
        (datetime(2023, 12, 31, tzinfo=utc), Frequency.YEARLY, "2022"),
        (datetime(2024, 9, 2, tzinfo=utc), Frequency.MONTHLY, "2024-07"),
        (datetime(2024, 9, 3, tzinfo=utc), Frequency.MONTHLY, "2024-08"),
        (datetime(2023, 12, 31, tzinfo=utc), Frequency.MONTHLY, "2023-11"),
        (datetime(2024, 9, 1, tzinfo=utc), Frequency.WEEKLY, "2024-08-25"),
        (datetime(2024, 8, 27, tzinfo=utc), Frequency.WEEKLY, "2024-08-25"),
        (datetime(2024, 8, 17, tzinfo=utc), Frequency.WEEKLY, "2024-08-11"),
        (datetime(2024, 9, 1, tzinfo=utc), Frequency.DAILY, "2024-08-30"),
        (datetime(2024, 1, 1, tzinfo=utc), Frequency.DAILY, "2023-12-30"),
        (datetime(2024, 8, 17, tzinfo=utc), Frequency.DAILY, "2024-08-15"),
    ],
    ids=[
        "year-2024-01-02",
        "year-2024-01-03",
        "year-2023-12-31",
        "month-2024-09-02",
        "month-2024-09-03",
        "month-2023-12-31",
        "week-2024-09-01",
        "week-2024-08-27",
        "week-2024-08-17",
        "day-2024-09-01",
        "day-2024-01-01",
        "day-2024-08-17",
    ],
)
def test_it(today, frequency, expected):
    actual = frequency.report_date(today=today)

    assert actual == expected
