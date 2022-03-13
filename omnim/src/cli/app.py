import asyncio
from pathlib import Path
from typing import Optional, List

import typer

from omnim.src.application.metrics import calculate_metrics_for_events
from omnim.src.configuration.config import Config
from omnim.src.loaders.csvloader import CsvEventsLoader
from omnim.src.metrics.leadtime import WorkflowEvent
from omnim.src.sources.github_actions import GithubActionsSource
from omnim.src.cli.metric import MetricsOptions

app = typer.Typer()


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

    events_loader = CsvEventsLoader(input_file)

    if source is not None:
        source = GithubActionsSource(config)
        asyncio.run(source.listen_source())
        events_loader = CsvEventsLoader(source.target)
        print("Successfully fetched workflow execution from github")

    try:
        events_loader.load()
        events: List[WorkflowEvent] = events_loader.get_all_events()
    except Exception as e:
        raise e

    if metrics is not None:
        calculate_metrics_for_events(metrics, events)


if __name__ == "__main__":
    app()
