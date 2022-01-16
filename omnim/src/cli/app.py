import typer
from enum import Enum

app = typer.Typer()


class MetricsOptions(Enum):
    LT = "lt"
    DF = "df"
    CFR = "cfr"
    MTTR = "mttr"


@app.command()
def main(
    metrics: MetricsOptions = typer.Option("", help=""),
    input_file: str = ""
):
    typer.echo(f"Hello")

if __name__ == "__main__":
    app()