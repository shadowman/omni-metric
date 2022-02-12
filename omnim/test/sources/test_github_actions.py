import os
from unittest.mock import patch

import pytest

from omnim.src.configuration.config import Config
from omnim.src.exceptions.exceptions import TokenNotFoundException
from omnim.src.sources.github_actions import GithubActionsSource


@pytest.fixture
def config():
    return Config()


class TestGithubActionsSource:
    @pytest.mark.parametrize("test_token", ["", None])
    async def test_should_raise_exception_if_no_token_provided(
        self, test_token, config
    ):

        with pytest.raises(TokenNotFoundException, match="Not token provided!"):
            config.token = test_token
            GithubActionsSource(config)

    async def test_should_store_nothing_if_no_events_happened_on_github(
        self, github_response, config
    ):
        noworkflow_response = {"total_count": 0, "workflow_runs": []}
        with patch(
            "omnim.src.sources.github_actions.GithubActionsSource._pull",
            return_value=noworkflow_response,
        ):
            pipe_source = GithubActionsSource(config)

            await pipe_source.listen_source()

            assert not os.path.isfile(pipe_source.target)

    async def test_should_store_events_from_github_when_pulling_in_a_target_file(  # noqa: E501
        self, github_response, config
    ):
        with patch(
            "omnim.src.sources.github_actions.GithubActionsSource._pull",
            return_value=github_response,
        ):
            pipe_source = GithubActionsSource(config)

            await pipe_source.listen_source()

            assert os.path.isfile(pipe_source.target)

    async def test_should_store_events_not_create_headers_in_a_target_file_if_it_already_exist(  # noqa: E501
        self, github_response, config
    ):

        with patch(
            "omnim.src.sources.github_actions.GithubActionsSource._pull",
            return_value=github_response,
        ):
            pipe_source = GithubActionsSource(config)
            expected_header = ",".join(pipe_source.field_names) + "\n"

            with open(pipe_source.target, "a", newline="") as csvfile:
                csvfile.write(expected_header)

            await pipe_source.listen_source()

            with open(pipe_source.target) as csvfile:
                content = csvfile.readlines()
                assert content[0] == expected_header and all(
                    [line != expected_header for line in content[1:]]
                )

    async def test_should_crash_when_github_client_raises_exception(
        self, github_response, config
    ):
        with patch(
            "omnim.src.sources.github_actions.GithubActionsSource._pull",
            return_value=Exception(),
        ):
            pipe_source = GithubActionsSource(config)

            with pytest.raises(Exception):
                await pipe_source.listen_source()
