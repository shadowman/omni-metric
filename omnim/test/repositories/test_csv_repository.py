import datetime
import os

import pytest

from omnim.src.configuration.config import Config
from omnim.src.metrics.leadtime import WorkflowEvent


@pytest.fixture
def config():
    return Config()


class CsvRepository:
    def __init__(self, target_file):
        self.target_file = target_file

    def save(self, events_stream):
        pass


class TestCsvRepository:
    def test_should_store_events_in_a_target_file(self, config):  # noqa: E501
        today = datetime.datetime.today()
        yesterday = today - datetime.timedelta(days=2)

        events_stream = (
            WorkflowEvent(yesterday, "build_failed"),
            WorkflowEvent(today, "deploy_success"),
        )
        target_file = "./data/stored_from_csv.csv"

        repository = CsvRepository(target_file)
        repository.save(events_stream)

        assert os.path.isfile(target_file)

    # async def test_should_store_events_not_create_headers_in_a_target_file_if_it_already_exist(  # noqa: E501
    #         self, github_response, config
    # ):
    #     with patch(
    #             "omnim.src.sources.github_actions.GithubActionsSource._pull",
    #             return_value=github_response,
    #     ):
    #         pipe_source = GithubActionsSource(config)
    #         expected_header = ",".join(pipe_source.field_names) + "\n"
    #
    #         with open(pipe_source.target, "a", newline="") as csvfile:
    #             csvfile.write(expected_header)
    #
    #         await pipe_source.listen_source()
    #
    #         with open(pipe_source.target) as csvfile:
    #             content = csvfile.readlines()
    #             assert content[0] == expected_header and all(
    #                 [line != expected_header for line in content[1:]]
    #             )
    #
