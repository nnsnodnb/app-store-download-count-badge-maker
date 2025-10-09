from pathlib import Path

import click

from . import __version__
from .appstore import sales_reports
from .badge import create_badges
from .config import Config, InvalidConfigError, parse_config


@click.group(name="app-store-download-count-badge-maker", invoke_without_command=True)
@click.version_option(
    __version__,
    "--version",
    "-V",
    prog_name="app-store-download-count-badge-maker",
)
def cli() -> None:
    pass


def _parse_config(config: str) -> Config:
    try:
        return parse_config(config=config)
    except InvalidConfigError as e:
        click.echo(e, err=True)
        raise click.exceptions.Exit(1) from e


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
    conf = _parse_config(config)

    reports = sales_reports(config=conf)

    output_dir = Path(output)
    output_dir.mkdir(exist_ok=True)
    create_badges(sales_reports=reports, download_dir=output_dir)

    click.echo(f"Generated badges in {output_dir}.")


@click.command(help="Generate index.html from config.yml.")
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
@click.option(
    "--force",
    "-f",
    is_flag=True,
    default=False,
    help="Overwrite existing index.html.",
)
def make_index(config: str, output: str, force: bool) -> None:
    conf = _parse_config(config)

    output_dir = Path(output)
    output_dir.mkdir(exist_ok=True)
    index_html_path = output_dir / "index.html"

    if index_html_path.exists() and not force:
        click.echo("index.html already exists. Use the ", nl=False)
        click.echo(click.style("--force", bold=True), nl=False)
        click.echo(" option to overwrite.", err=True)
        raise click.exceptions.Exit(1)

    text = conf.make_index_html_text()
    index_html_path.write_text(text, encoding="utf-8")

    click.echo(f"Generated index.html in {output_dir}.")


cli.add_command(generate)
cli.add_command(make_index)


if __name__ == "__main__":
    cli()
