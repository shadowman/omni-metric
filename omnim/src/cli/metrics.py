from pathlib import Path
from typing import List, Optional

import typer

from omnim.src.application.metrics import calculate_metrics_for_events
from omnim.src.cli.metric import MetricsOptions
from omnim.src.loaders.csvloader import CsvEventsLoader
from omnim.src.metrics.leadtime import WorkflowEvent


def metrics(
    metrics: Optional[MetricsOptions] = typer.Option(None, help=""),
    input_file: Optional[Path] = typer.Option(None, exists=True, file_okay=True),
):
    events_loader = CsvEventsLoader(input_file)

    try:
        events_loader.load()
        events: List[WorkflowEvent] = events_loader.get_all_events()
    except Exception as e:
        raise e

    if metrics is not None:
        calculate_metrics_for_events(metrics, events)
