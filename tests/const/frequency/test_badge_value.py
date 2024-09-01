import pytest

from maker.const import Frequency


@pytest.mark.parametrize(
    "frequency, expected",
    [
        (Frequency.YEARLY, "year"),
        (Frequency.MONTHLY, "month"),
        (Frequency.WEEKLY, "week"),
        (Frequency.DAILY, "day"),
    ],
    ids=["yearly", "monthly", "weekly", "daily"],
)
def test_it(frequency, expected):
    assert frequency.badge_value == expected
