import typer
from enum import Enum
from pathlib import Path

app = typer.Typer()


class MetricsOptions(Enum):
    LT = "lt"
    DF = "df"
    CFR = "cfr"
    MTTR = "mttr"


@app.command()
def main(
    metrics: MetricsOptions = typer.Option(..., help=""),
    input_file: Path = typer.Option(..., exists=True, file_okay=True)
):
    # TODO: Implement
    pass


if __name__ == "__main__":
    app()
