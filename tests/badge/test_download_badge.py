from pathlib import Path

import pytest

from maker.appstore import SalesReport
from maker.badge import download_badge
from maker.config import App
from maker.const import Frequency


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

    sales_report = SalesReport(units=210, app=App(apple_identifier=1, frequency=Frequency.MONTHLY))
    await download_badge(sales_report=sales_report, download_dir=tmp_path)
