import asyncio
from pathlib import Path
from typing import List

from httpx import AsyncClient

from .appstore import SalesReport

BASE_URL = "https://img.shields.io/badge"


def create_badge_url(sales_report: SalesReport) -> str:
    unit_per_frequency = sales_report.units_per_frequency().replace("/", "%2F")
    color = sales_report.get_badge_color()
    right = f"{unit_per_frequency}-{color.value}"
    badge_url = f"{BASE_URL}/download-{right}"

    return badge_url


async def download_badge(sales_report: SalesReport, download_dir: Path) -> None:
    badge_url = create_badge_url(sales_report=sales_report)

    async with AsyncClient() as client:
        res = await client.get(badge_url)

    badge_filename = f"{sales_report.app.apple_identifier}-{sales_report.app.frequency.badge_value}.svg"
    badge_path = download_dir / badge_filename

    badge_path.write_bytes(res.content)


async def download_badges(sales_reports: List[SalesReport], download_dir: Path) -> None:
    tasks = [download_badge(sales_report=sales_report, download_dir=download_dir) for sales_report in sales_reports]
    await asyncio.gather(*tasks)


def create_badges(sales_reports: List[SalesReport], download_dir: Path) -> None:
    asyncio.run(download_badges(sales_reports=sales_reports, download_dir=download_dir))
