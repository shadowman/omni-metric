import datetime
import os
from pathlib import Path

import pytest

from omnim.src.events import EventType
from omnim.src.metrics.leadtime import WorkflowEvent
from omnim.src.repositories.csv_repository import CsvRepository


class TestCsvRepository:
    def test_it_should_set_a_parametrized_file_to_be_loaded(self):
        loader = CsvRepository("test")
        assert loader.target_file == "test"

    def test_it_should_throw_exception_if_file_not_found(self):
        loader = CsvRepository("test")
        with pytest.raises(FileNotFoundError):
            loader.load()

    def test_should_store_events_in_a_target_file(
        self, config, csv_environment
    ):  # noqa: E501
        today = datetime.datetime.today()
        yesterday = today - datetime.timedelta(days=2)

        events_stream = WorkflowEvent(yesterday, EventType.BUILD_FAILED)

        target_file = "./data/stored_from_csv.csv"

        repository = CsvRepository(Path(target_file))
        repository.save(events_stream)

        assert os.path.isfile(target_file)

    def test_should_store_events_not_create_headers_in_a_target_file_if_it_already_exist(  # noqa: E501
        self, config, csv_environment
    ):

        expected_header = ",".join(["datetime", "event_name", "data"]) + "\n"
        events_stream = WorkflowEvent(datetime.datetime.today(), EventType.BUILD_FAILED)

        target_file = "./data/stored_from_csv.csv"

        repository = CsvRepository(Path(target_file))
        repository.save(events_stream)

        with open(repository.target_file) as csvfile:
            content = csvfile.readlines()

            assert content[0] == expected_header
            assert all([line != expected_header for line in content[1:]])
