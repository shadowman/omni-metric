import typer
from typing import Optional
from enum import Enum
from pathlib import Path
import json

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
from omnim.src.configuration.config import Config
app = typer.Typer()


class MetricsOptions(Enum):
    LT = "lt"
    DF = "df"
    CFR = "cfr"
    MTTR = "mttr"


@app.command()
def main(
    config_file: Optional[Path] = typer.Option(None),
    metrics: Optional[MetricsOptions] = typer.Option(None, help=""),
    input_file: Optional[Path] = typer.Option(None, exists=True, file_okay=True),
    source: Optional[str] = typer.Option(None),
    fetch: Optional[str] = typer.Option(None)
):

    config = Config()
    if config_file is not None:
        # config = Config(config_file)
        #config = OminimetricConfiguation(config_file)
        print(f"Using '{config_file}' as config file")
        
    
    if source is not None:
        # source = GithubActionsSource(source, config)
        # source.fetch()
        print("Successfully fetched workflow execution from github")

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
