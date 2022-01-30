import typer
from enum import Enum
from pathlib import Path

from omnim.src.metrics.csvloader import CsvEventsLoader
from omnim.src.metrics.leadtime import LeadtimeMetricCalculator
from omnim.src.metrics.deployment_frequency import (
    DeploymentFrequencyMetricCalculator
)
from omnim.src.metrics.change_failure_rate import (
    ChangeFailureRateMetricCalculator
)
from omnim.src.metrics.mean_time_to_restore import (
    MeanTimeToRestoreMetricCalculator
)

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
    if metrics == MetricsOptions.LT:
        calculator = LeadtimeMetricCalculator()
    elif metrics == MetricsOptions.DF:
        calculator = DeploymentFrequencyMetricCalculator()
    elif metrics == MetricsOptions.CFR:
        calculator = ChangeFailureRateMetricCalculator()
    elif metrics == MetricsOptions.MTTR:
        calculator = MeanTimeToRestoreMetricCalculator()

    events_loader = CsvEventsLoader(input_file)

    try:
        events_loader.load()
        events = events_loader.get_all_events()
    except Exception as e:
        raise e

    output = calculator.calculate(events)

    if metrics == MetricsOptions.LT:
        print(
            "Average Build to Deploy Leadtime =",
            output.total_seconds(),
            "s"
        )
    elif metrics == MetricsOptions.DF:
        print(f"Average Deployment Frequency = {output} dep/day")
    elif metrics == MetricsOptions.CFR:
        print(f"Average Change Failure Rate = {output} failures/dep")
    elif metrics == MetricsOptions.MTTR:
        if output is None:
            print("Not enough data to calculate Mean Time To Restore")
        else:
            print(f"Mean Time To Restore = {output} second(s)")


if __name__ == "__main__":
    app()
