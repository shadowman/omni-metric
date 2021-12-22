from omnim.src.sources.github_actions import GithubActionsSource
import pytest
import asynctest
import os


class TestGithubActions:

    @pytest.mark.asyncio
    async def test_should_store_nothing_if_no_events_happened_on_github(
            self,
            github_response
    ):
        noworkflow_response = {"total_count": 0, "workflow_runs": []}
        with asynctest.patch(
                "omnim.src.sources.github_actions.GithubActionsSource._pull",
                return_value=noworkflow_response
        ):
            pipe_source = GithubActionsSource(
                user="jmaralc",
                repo="oop_rust",
                deployment_action_name="Greetings"
            )

            await pipe_source.listen_source()

            assert not os.path.isfile(pipe_source.target)

    @pytest.mark.asyncio
    async def test_should_store_events_from_github_when_pulling_in_a_target_file(  # noqa: E501
            self,
            github_response
    ):
        with asynctest.patch(
                "omnim.src.sources.github_actions.GithubActionsSource._pull",
                return_value=github_response
        ):
            pipe_source = GithubActionsSource(
                user="jmaralc",
                repo="oop_rust",
                deployment_action_name="Greetings"
            )

            await pipe_source.listen_source()

            assert os.path.isfile(pipe_source.target)

    @pytest.mark.asyncio
    async def test_should_crash_when_github_client_raises_exception(
            self,
            github_response
    ):
        with asynctest.patch(
                "omnim.src.sources.github_actions.GithubActionsSource._pull",
                return_value=Exception()
        ):
            pipe_source = GithubActionsSource(
                user="jmaralc",
                repo="oop_rust",
                deployment_action_name="Greetings"
            )

            with pytest.raises(Exception):
                await pipe_source.listen_source()
