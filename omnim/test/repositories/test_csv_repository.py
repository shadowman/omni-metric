import csv
import datetime
import os
from pathlib import Path
from typing import List

import pytest

from omnim.src.configuration.config import Config
from omnim.src.metrics.leadtime import WorkflowEvent


@pytest.fixture
def config():
    return Config()


@pytest.fixture(scope="function")
def csv_environment():
    # Tear up
    yield None

    # Tear down
    if os.path.isfile("./data/stored_from_csv.csv"):
        os.remove("./data/stored_from_csv.csv")


class CsvRepository:
    field_names: List[str] = ["datetime", "event_name", "data"]

    def __init__(self, target_file: str):
        self.target_file = Path(target_file)

    def save(self, events_stream: WorkflowEvent):
        if not self.target_file.is_file():
            with open(self.target_file, "a", newline="") as csvfile:

                writer = csv.DictWriter(csvfile, fieldnames=self.field_names)
                writer.writeheader()

        with open(self.target_file, "a", newline="") as csvfile:
            csv_row_writer = csv.writer(
                csvfile,
                delimiter=",",
                quotechar="|",
                quoting=csv.QUOTE_MINIMAL,
            )
            csv_row_writer.writerow(
                [events_stream.datetime, events_stream.type, events_stream.data]
            )


class TestCsvRepository:
    def test_should_store_events_in_a_target_file(
        self, config, csv_environment
    ):  # noqa: E501
        today = datetime.datetime.today()
        yesterday = today - datetime.timedelta(days=2)

        events_stream = WorkflowEvent(yesterday, "build_failed")

        target_file = "./data/stored_from_csv.csv"

        repository = CsvRepository(target_file)
        repository.save(events_stream)

        assert os.path.isfile(target_file)

    def test_should_store_events_not_create_headers_in_a_target_file_if_it_already_exist(  # noqa: E501
        self, config, csv_environment
    ):

        expected_header = ",".join(["datetime", "event_name", "data"]) + "\n"
        events_stream = WorkflowEvent(datetime.datetime.today(), "build_failed")

        target_file = "./data/stored_from_csv.csv"

        repository = CsvRepository(target_file)
        repository.save(events_stream)

        with open(repository.target_file) as csvfile:
            content = csvfile.readlines()

            assert content[0] == expected_header
            assert all([line != expected_header for line in content[1:]])
