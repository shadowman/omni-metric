import datetime
import os
from pathlib import Path

import pytest
from omnim.src.events import EventType
from omnim.src.metrics.leadtime import WorkflowEvent
from omnim.src.repositories.csv_repository import CsvRepository


class TestCsvRepository:
    def setup(self):
        self.test_csv_loader = CsvRepository(Path("./data/sample.csv"))

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

    def test_it_should_load_each_row_as_a_workflow_event(self):
        self.test_csv_loader.load()

        events = self.test_csv_loader.get_all_events()

        assert 3 == len(events)

    @pytest.mark.skip
    def test_it_should_load_each_event_date_and_time_correctly(self):
        self.test_csv_loader.load()

        events = self.test_csv_loader.get_all_events()

        for event in events:
            assert isinstance(event.datetime, type(datetime))

    def test_it_should_load_event_names_correctly(self):
        self.test_csv_loader.load()

        events = self.test_csv_loader.get_all_events()

        first_event = events[0]
        assert first_event.event_type == EventType.BUILD_SUCCESS

    def test_it_should_load_each_event_data_correctly(self):
        self.test_csv_loader.load()

        events = self.test_csv_loader.get_all_events()

        first_event = events[0]
        assert first_event.data == "pipeline_id1#1"
