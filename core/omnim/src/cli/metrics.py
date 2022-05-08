import datetime
from pathlib import Path
from typing import List, Optional

import typer
from omnim.src.application.metrics import calculate_metrics_for_events
from omnim.src.cli.metric import MetricsOptions
from omnim.src.metrics.leadtime import WorkflowEvent
from omnim.src.repositories.csv_repository import CsvRepository


def metrics(
    metrics: Optional[MetricsOptions] = typer.Option(None, help=""),
    input_file: Optional[Path] = typer.Option(
        None,
        exists=True,
        file_okay=True,
    ),
    start: Optional[str] = typer.Option(None),
):
    if input_file is None:
        return None

    events_loader = CsvRepository(input_file)

    start_timestamp = None
    if start is not None:
        start_timestamp = datetime.datetime.strptime(start, "%Y-%m-%d")

    try:
        events_loader.load(start=start_timestamp)
        events: List[WorkflowEvent] = events_loader.get_all_events()
    except Exception as e:
        raise e

    if metrics is not None:
        calculate_metrics_for_events(metrics, events)
