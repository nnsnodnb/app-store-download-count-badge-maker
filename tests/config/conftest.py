from pathlib import Path

import pytest

from maker.config import App, Config, parse_config
from maker.const import BadgeStyle, Frequency


@pytest.fixture(scope="session")
def config_path() -> str:
    path = Path(__file__).parent / "config.yml"
    return str(path)


@pytest.fixture(scope="session")
def config(config_path: str) -> Config:
    config = parse_config(config_path)
    yield config

    assert (
        config.secrets.private_key
        == "-----BEGIN PRIVATE KEY-----\ndummydummydummydummydummydummy\n-----END PRIVATE KEY-----\n"
    )
    assert config.secrets.issuer_id == "12345678-1234-1234-1234-123456789012"
    assert config.secrets.key_id == 12345678
    assert config.secrets.vendor_number == 12345678
    assert config.apps == [
        App(apple_identifier=1289764391, frequency=Frequency.MONTHLY, badge_style=BadgeStyle.FLAT),
        App(apple_identifier=1234567890, frequency=Frequency.WEEKLY, badge_style=BadgeStyle.FLAT_SQUARE),
        App(apple_identifier=1234567890, frequency=Frequency.DAILY, badge_style=BadgeStyle.PLASTIC),
        App(apple_identifier=1234567890, frequency=Frequency.YEARLY, badge_style=BadgeStyle.FOR_THE_BADGE),
        App(apple_identifier=1234567890, frequency=Frequency.YEARLY, badge_style=BadgeStyle.SOCIAL),
    ]
