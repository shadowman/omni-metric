import typer
from omnim.src.cli.fetch import fetch
from omnim.src.cli.metrics import metrics

app = typer.Typer()

app.command()(fetch)
app.command()(metrics)


if __name__ == "__main__":
    app()
