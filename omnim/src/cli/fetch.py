import asyncio
from pathlib import Path
from typing import List, Optional

import typer

from omnim.src.application.metrics import calculate_metrics_for_events
from omnim.src.cli.metric import MetricsOptions
from omnim.src.configuration.config import Config
from omnim.src.loaders.csvloader import CsvEventsLoader
from omnim.src.metrics.leadtime import WorkflowEvent
from omnim.src.sources.github_actions import GithubActionsSource


def fetch(
    config_file: Optional[Path] = typer.Option(None),
    metrics: Optional[MetricsOptions] = typer.Option(None, help=""),
    input_file: Optional[Path] = typer.Option(None, exists=True, file_okay=True),
    source: Optional[str] = typer.Option(None),
    fetch: Optional[str] = typer.Option(None),
):
    # destination_storage = Path("./data/result.csv")

    config = Config()
    if config_file is not None:
        print(f"Using '{config_file}' as config file")
        config = Config(config_file)
        print(f"Configuration set to use: {config.storage_type} storage")

    events_loader = CsvEventsLoader(input_file)

    if source is not None:
        git_source = GithubActionsSource(config)
        asyncio.run(git_source.listen_source())
        events_loader = CsvEventsLoader(git_source.target)
        print("Successfully fetched workflow execution from github")

    try:
        events_loader.load()
        events: List[WorkflowEvent] = events_loader.get_all_events()
    except Exception as e:
        raise e

    if metrics is not None:
        calculate_metrics_for_events(metrics, events)
