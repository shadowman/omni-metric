from omnim.src.sources.github_actions import GithubActionsSource
import pytest


class TestGithubActions:

    @pytest.mark.asyncio
    async def test_should_return_information_about_latest_actions_status(self):
        pipe_source = GithubActionsSource(
            user="jmaralc",
            repo="oop_rust"
        )

        pipe_source.listen_source()
