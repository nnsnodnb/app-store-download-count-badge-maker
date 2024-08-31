from dataclasses import dataclass
from pathlib import Path
from typing import List

import yaml

from .const import Frequency


class InvalidConfigError(Exception):
    pass


@dataclass(frozen=True)
class Secrets:
    private_key: str
    issuer_id: str
    key_id: str
    vendor_number: int


@dataclass(frozen=True)
class App:
    apple_identifier: int
    frequency: Frequency


@dataclass(frozen=True)
class Config:
    secrets: Secrets
    apps: List[App]


def parse_config(config: str) -> Config:
    with Path(config).open("r") as f:
        data = yaml.safe_load(f)

    try:
        raw_secrets = data["secrets"]
    except KeyError:
        raise InvalidConfigError("Missing 'secrets' key in the configuration file.")

    try:
        private_key = Path(raw_secrets["private_key"]).read_text()
    except (KeyError, FileNotFoundError):
        raise InvalidConfigError("Invalid the configuration file.")

    try:
        secrets = Secrets(
            private_key=private_key,
            issuer_id=raw_secrets["issuer_id"],
            key_id=raw_secrets["key_id"],
            vendor_number=raw_secrets["vendor_number"],
        )
    except KeyError:
        raise InvalidConfigError("Invalid the configuration file.")

    try:
        raw_apps = data["apps"]
        apps = []
        for app in raw_apps:
            try:
                frequency = Frequency(app["frequency"])
            except KeyError:
                raise InvalidConfigError("Missing 'frequency' key in the configuration file.")
            except ValueError:
                raise InvalidConfigError("Invalid 'frequency' value in the configuration file.")
            apps.append(App(apple_identifier=app["apple_identifier"], frequency=frequency))
    except KeyError:
        raise InvalidConfigError("Missing 'apps' key in the configuration file.")

    return Config(secrets=secrets, apps=apps)
