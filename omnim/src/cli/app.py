import typer
from enum import Enum
from pathlib import Path

from omnim.src.metrics.csvloader import CsvEventsLoader
from omnim.src.metrics.leadtime import LeadtimeMetricCalculator

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
    events_loader = CsvEventsLoader(input_file)

    try:
        events_loader.load()
        events = events_loader.get_all_events()
    except Exception as e:
        raise e

    result = LeadtimeMetricCalculator()
    output = result.calculate(events)

    print(
        "Average Build to Deploy Leadtime =",
        output.total_seconds(),
        "s"
    )


if __name__ == "__main__":
    app()
