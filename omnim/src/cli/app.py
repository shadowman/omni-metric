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

app = typer.Typer()


if __name__ == "__main__":
    app()
