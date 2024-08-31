from pathlib import Path

import click

from . import __version__
from .appstore import AppStoreConnectError, sales_reports
from .badge import create_badges
from .config import InvalidConfigError, parse_config


@click.group(name="app-store-download-count-badge-maker", invoke_without_command=True)
@click.version_option(
    __version__,
    "--version",
    "-V",
    prog_name="app-store-download-count-badge-maker",
)
def cli() -> None:
    pass


@click.command(help="Generate badges for the App Store download count.")
@click.help_option("--help")
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    default="config.yml",
    help="Path to the configuration file.",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(file_okay=False),
    default="dist",
    help="Path to the output directory. default is dist.",
)
def generate(config: str, output: str) -> None:
    try:
        conf = parse_config(config=config)
    except InvalidConfigError as e:
        click.echo(e, err=True)
        raise click.exceptions.Exit(1)
    except AppStoreConnectError as e:
        click.echo(e, err=True)
        raise click.exceptions.Exit(2)

    reports = sales_reports(config=conf)

    output_dir = Path(output)
    output_dir.mkdir(exist_ok=True)
    create_badges(sales_reports=reports, download_dir=output_dir)

    click.echo(f"Generated badges in {output_dir}", color=True)


cli.add_command(generate)


if __name__ == "__main__":
    cli()
