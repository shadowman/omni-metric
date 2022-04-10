import asyncio
from pathlib import Path
from typing import Optional

import typer

from omnim.src.configuration.config import Config
from omnim.src.repositories.csv_repository import CsvRepository
from omnim.src.sources.github_actions import GithubActionsSource


def fetch(
    config_file: Optional[Path] = typer.Option(None),
    input_file: Path = typer.Option(None, exists=True, file_okay=True),
    source: Optional[str] = typer.Option(None),
):
    config = Config()
    if config_file is not None:
        print(f"Using '{config_file}' as config file")
        config = Config(config_file)
        print(f"Configuration set to use: {config.storage_type} storage")

    events_loader = CsvRepository(input_file)

    if source is not None:
        git_source = GithubActionsSource(config)
        asyncio.run(git_source.listen_source())
        events_loader = CsvRepository(Path(git_source.target))
        print("Successfully fetched workflow execution from github")

    try:
        events_loader.load()
    except Exception as e:
        raise e
