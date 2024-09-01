import asyncio
import gzip
import io
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Set

import httpx
import jwt
import pandas as pd
from httpx import AsyncClient

from .config import App, Config, Frequency, Secrets
from .const import Color


@dataclass(frozen=True)
class SalesReport:
    units: int
    app: App

    def units_per_frequency(self) -> str:
        return f"{self.units_normalize()}/{self.app.frequency.badge_value}"

    def units_normalize(self) -> str:
        if self.units >= 1_000_000:
            units = f"{self.units / 1_000_000:.1f}"
            int_part, dec_part = units.split(".")
            if dec_part == "0":
                return f"{int_part}M"
            else:
                return f"{units}M"
        elif self.units >= 1_000:
            units = f"{self.units / 1_000:.1f}"
            int_part, dec_part = units.split(".")
            if dec_part == "0":
                return f"{int_part}k"
            else:
                return f"{units}k"
        else:
            return str(self.units)

    def get_badge_color(self) -> Color:
        if self.units == 0:
            return Color.RED
        elif self.units < 10:
            return Color.YELLOW
        elif self.units < 100:
            return Color.YELLOWGREEN
        elif self.units < 1000:
            return Color.GREEN
        else:
            return Color.BRIGHTGREEN


class AppStoreConnectError(Exception):
    pass


def gen_token(secrets: Secrets) -> str:
    iat = int(datetime.now().timestamp())
    token = jwt.encode(
        payload={
            "iss": secrets.issuer_id,
            "iat": iat,
            "exp": iat + 200,
            "aud": "appstoreconnect-v1",
        },
        key=secrets.private_key,
        algorithm="ES256",
        headers={
            "alg": "ES256",
            "kid": secrets.key_id,
        },
    )
    return token


async def get_sales_reports_with_frequency(secrets: Secrets, frequency: Frequency, download_dir: Path) -> Optional[int]:
    token = gen_token(secrets)
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "*/*",
    }
    params = {
        "filter[frequency]": frequency.value,
        "filter[reportDate]": frequency.report_date(today=datetime.today()),
        "filter[reportSubType]": "SUMMARY",
        "filter[reportType]": "SALES",
        "filter[vendorNumber]": secrets.vendor_number,
    }

    async with AsyncClient(params=params, headers=headers) as client:
        url = "https://api.appstoreconnect.apple.com/v1/salesReports"
        res = await client.get(url)

    try:
        res.raise_for_status()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == httpx.codes.NOT_FOUND:
            return 0
        else:
            raise AppStoreConnectError from e

    with gzip.open(io.BytesIO(res.content), "rb") as f:
        data = f.read()

    tsv_path = download_dir / f"{secrets.vendor_number}_{frequency.value.lower()}.tsv"
    tsv_path.write_bytes(data)

    return None


async def download_sales_reports(secrets: Secrets, frequencies: Set[Frequency], download_dir: Path) -> None:
    tasks = [
        get_sales_reports_with_frequency(secrets=secrets, frequency=frequency, download_dir=download_dir)
        for frequency in frequencies
    ]
    await asyncio.gather(*tasks)


def parse_tsv(tsv_path: Path, apple_identifier: int) -> int:
    df = pd.read_csv(tsv_path, sep="\t")
    units_sum = df[df["Apple Identifier"] == apple_identifier]["Units"].sum().item()
    return units_sum


def get_sales_reports(secrets: Secrets, app: App, download_dir: Path) -> SalesReport:
    tsv_path = download_dir / f"{secrets.vendor_number}_{app.frequency.value.lower()}.tsv"
    if not tsv_path.exists():
        return SalesReport(units=0, app=app)

    units = parse_tsv(tsv_path=tsv_path, apple_identifier=app.apple_identifier)
    return SalesReport(units=units, app=app)


def sales_reports(config: Config) -> List[SalesReport]:
    with tempfile.TemporaryDirectory() as tmpdir:
        download_dir = Path(tmpdir)

        frequencies = set(app.frequency for app in config.apps)
        asyncio.run(
            download_sales_reports(
                secrets=config.secrets,
                frequencies=frequencies,
                download_dir=download_dir,
            )
        )

        reports = [get_sales_reports(secrets=config.secrets, app=app, download_dir=download_dir) for app in config.apps]

    return reports
