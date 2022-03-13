import asyncio
from enum import Enum
from pathlib import Path
from typing import Optional

import typer

from omnim.src.configuration.config import Config
from omnim.src.loaders.csvloader import CsvEventsLoader
from omnim.src.metrics.change_failure_rate import \
    ChangeFailureRateMetricCalculator
from omnim.src.metrics.deployment_frequency import \
    DeploymentFrequencyMetricCalculator
from omnim.src.metrics.leadtime import LeadtimeMetricCalculator
from omnim.src.metrics.mean_time_to_restore import \
    MeanTimeToRestoreMetricCalculator
from omnim.src.metrics.metric_result import MetricResult
from omnim.src.sources.github_actions import GithubActionsSource

app = typer.Typer()


class MetricsOptions(Enum):
    LEAD_TIME = "lt"
    DEPLOYMENT_FREQUENCY = "df"
    CHANGE_FAILURE_RATE = "cfr"
    MEAN_TIME_TO_RESTORE = "mttr"


@app.command(
    no_args_is_help=True
)
def main(
    config_file: Optional[Path] = typer.Option(None),
    metrics: Optional[MetricsOptions] = typer.Option(None, help=""),
    input_file: Optional[Path] = typer.Option(None, exists=True, file_okay=True),
    source: Optional[str] = typer.Option(None),
    fetch: Optional[str] = typer.Option(None),
):

    config = Config()
    if config_file is not None:
        config = Config(config_file)
        print(f"Using '{config_file}' as config file")

    availableMetrics = {
        MetricsOptions.LEAD_TIME: LeadtimeMetricCalculator,
        MetricsOptions.DEPLOYMENT_FREQUENCY: DeploymentFrequencyMetricCalculator
    }

    calculator = availableMetrics.get(metrics, lambda: None)()

    if metrics == MetricsOptions.CHANGE_FAILURE_RATE:
        calculator = ChangeFailureRateMetricCalculator()
    elif metrics == MetricsOptions.MEAN_TIME_TO_RESTORE:
        calculator = MeanTimeToRestoreMetricCalculator()

    events_loader = CsvEventsLoader(input_file)

    if source is not None:
        source = GithubActionsSource(config)
        asyncio.run(source.listen_source())
        events_loader = CsvEventsLoader(source.target)
        print("Successfully fetched workflow execution from github")

    try:
        events_loader.load()
        events = events_loader.get_all_events()
    except Exception as e:
        raise e

    if calculator is not None:
        output: MetricResult = calculator.calculate(events)
        output.report()


if __name__ == "__main__":
    app()
