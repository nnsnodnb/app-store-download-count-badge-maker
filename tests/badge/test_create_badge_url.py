import pytest

from maker.appstore import SalesReport
from maker.badge import create_badge_url
from maker.config import App
from maker.const import BadgeStyle, Frequency


@pytest.mark.parametrize(
    "badge_style, expected",
    [
        (badge_style, f"https://img.shields.io/badge/download-123%2Fday-green?style={badge_style.value}")
        for badge_style in BadgeStyle
    ],
    ids=[badge_style.value for badge_style in BadgeStyle],
)
def test_it(badge_style, expected):
    report = SalesReport(units=123, app=App(apple_identifier=1, frequency=Frequency.DAILY, badge_style=badge_style))
    actual = create_badge_url(sales_report=report)

    assert actual == expected
