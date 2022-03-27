import datetime
import os

from omnim.src.metrics.leadtime import WorkflowEvent
from omnim.src.repositories.csv_repository import CsvRepository


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
