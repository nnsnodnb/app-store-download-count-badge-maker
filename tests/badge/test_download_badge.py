from pathlib import Path

import pytest
from httpx import AsyncClient

from maker.appstore import SalesReport
from maker.badge import download_badge
from maker.config import App
from maker.const import BadgeStyle, Frequency


@pytest.fixture()
def svg_bytes():
    path = Path(__file__).parent / "dummy.svg"
    return path.read_bytes()


@pytest.mark.asyncio
async def test_it(tmp_path, httpx_mock, svg_bytes):
    httpx_mock.add_response(
        status_code=200,
        content=svg_bytes,
    )

    sales_report = SalesReport(
        units=210, app=App(apple_identifier=1, frequency=Frequency.MONTHLY, badge_style=BadgeStyle.FLAT)
    )
    await download_badge(client=AsyncClient(), sales_report=sales_report, download_dir=tmp_path)
    path = tmp_path / f"{sales_report.app.apple_identifier}-{sales_report.app.frequency.badge_value}.svg"

    assert path.exists()
