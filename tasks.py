from pathlib import Path

from invoke import task

BASE_DIR = Path(__file__).parent


@task
def format(ctx):
    with ctx.cd(BASE_DIR):
        ctx.run("black .")
        ctx.run("isort .")
