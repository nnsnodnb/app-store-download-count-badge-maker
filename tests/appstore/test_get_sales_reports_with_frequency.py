import pytest

from maker.appstore import Secrets, get_sales_reports_with_frequency
from maker.const import Frequency


@pytest.mark.asyncio
async def test_success(tmp_path, mocker, httpx_mock):
    mocker.patch("maker.appstore.gen_token", return_value="dummy_token")
    httpx_mock.add_response(status_code=200)

    result = await get_sales_reports_with_frequency(
        secrets=Secrets(
            private_key="private_key",
            issuer_id="issuer_id",
            key_id="key_id",
            vendor_number=12,
        ),
        frequency=Frequency.DAILY,
        download_dir=tmp_path,
    )

    assert result is None
    download_filepath = tmp_path / f"{12}_{Frequency.DAILY.value.lower()}.tsv"
    assert download_filepath.exists()


@pytest.mark.asyncio
async def test_not_found(tmp_path, mocker, httpx_mock):
    mocker.patch("maker.appstore.gen_token", return_value="dummy_token")
    httpx_mock.add_response(status_code=404)

    result = await get_sales_reports_with_frequency(
        secrets=Secrets(
            private_key="private_key",
            issuer_id="issuer_id",
            key_id="key_id",
            vendor_number=12,
        ),
        frequency=Frequency.DAILY,
        download_dir=tmp_path,
    )

    assert result == 0
    download_filepath = tmp_path / f"{12}_{Frequency.DAILY.value.lower()}.tsv"
    assert not download_filepath.exists()
