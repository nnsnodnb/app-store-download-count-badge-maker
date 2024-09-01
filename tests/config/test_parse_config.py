from pathlib import Path

import pytest

from maker.appstore import App
from maker.config import parse_config
from maker.const import Frequency


@pytest.fixture()
def config_path() -> str:
    path = Path(__file__).parent / "config.yml"
    return str(path)


def test_it(config_path):
    config = parse_config(config=config_path)

    assert (
        config.secrets.private_key
        == "-----BEGIN PRIVATE KEY-----\ndummydummydummydummydummydummy\n-----END PRIVATE KEY-----\n"
    )
    assert config.secrets.issuer_id == "12345678-1234-1234-1234-123456789012"
    assert config.secrets.key_id == 12345678
    assert config.secrets.vendor_number == 12345678
    assert config.apps == [
        App(apple_identifier=1289764391, frequency=Frequency.MONTHLY),
        App(apple_identifier=1234567890, frequency=Frequency.WEEKLY),
        App(apple_identifier=1234567890, frequency=Frequency.DAILY),
        App(apple_identifier=1234567890, frequency=Frequency.YEARLY),
    ]
