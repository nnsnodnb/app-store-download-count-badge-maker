from maker.appstore import SalesReport
from maker.badge import create_badge_url
from maker.config import App
from maker.const import Frequency


def test_it():
    report = SalesReport(units=123, app=App(apple_identifier=1, frequency=Frequency.DAILY))
    actual = create_badge_url(sales_report=report)

    assert actual == "https://img.shields.io/badge/download-123%2Fday-green"
