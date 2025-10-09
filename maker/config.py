from dataclasses import dataclass
from pathlib import Path

import yaml

from .const import BadgeStyle, Frequency


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
    badge_style: BadgeStyle


@dataclass(frozen=True)
class Config:
    secrets: Secrets
    apps: list[App]

    def make_index_html_text(self) -> str:
        def get_badge_name(app: App) -> str:
            return f"{app.apple_identifier}-{app.frequency.badge_value}.svg"

        badges = [get_badge_name(app) for app in self.apps]

        li_tags = "".join(f'<li><a href="./{badge}">{badge}</a></li>' for badge in badges)
        ul_tag = f"<ul>{li_tags}</ul>"
        html = f"<!DOCTYPE html><html><body>{ul_tag}</body></html>"

        return html


def parse_config(config: str) -> Config:
    with Path(config).open("r") as f:
        data = yaml.safe_load(f)

    try:
        raw_secrets = data["secrets"]
    except KeyError as e:
        raise InvalidConfigError("Missing 'secrets' key in the configuration file.") from e

    try:
        private_key = Path(raw_secrets["private_key"]).read_text()
    except (KeyError, FileNotFoundError) as e:
        raise InvalidConfigError("Invalid the configuration file.") from e

    try:
        secrets = Secrets(
            private_key=private_key,
            issuer_id=raw_secrets["issuer_id"],
            key_id=raw_secrets["key_id"],
            vendor_number=raw_secrets["vendor_number"],
        )
    except KeyError as e:
        raise InvalidConfigError("Invalid the configuration file.") from e

    try:
        raw_apps = data["apps"]
        apps = []
        for app in raw_apps:
            # Frequency
            try:
                frequency = Frequency(app["frequency"])
            except KeyError as e:
                raise InvalidConfigError("Missing 'frequency' key in the configuration file.") from e
            except ValueError as e:
                raise InvalidConfigError("Invalid 'frequency' value in the configuration file.") from e
            # BadgeStyle
            if (raw_bs := app.get("badge_style")) is not None:
                try:
                    badge_style = BadgeStyle(raw_bs)
                except ValueError as e:
                    raise InvalidConfigError("Invalid 'badge_style' value in the configuration file.") from e
            else:
                badge_style = BadgeStyle.FLAT

            apps.append(App(apple_identifier=app["apple_identifier"], frequency=frequency, badge_style=badge_style))
    except KeyError as e:
        raise InvalidConfigError("Missing 'apps' key in the configuration file.") from e

    return Config(secrets=secrets, apps=apps)
