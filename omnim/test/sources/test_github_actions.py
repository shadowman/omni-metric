from omnim.src.sources.github_actions import GithubPullActionsRun
import json

class TestGithubPullActionsRun:

    def test_should_be_empty_when_pull_returns_no_entries(self):
        settings = {
          "branch": "main"
        }

        actions_run = open("./data/github/actions_run_empty.json")
        github_api_response = json.load(actions_run)
      
        source = GithubPullActionsRun(settings, github_api_response)

        workflowRuns = source.pull()

        assert len(workflowRuns) == 0

    def test_should_pull_single_entry_from_given_branch(self):
        settings = {
          "branch": "main"
        }

        actions_run = open("./data/github/actions_single_run.json")
        github_api_response = json.load(actions_run)
      
        source = GithubPullActionsRun(settings, github_api_response)

        workflowRuns = source.pull()

        assert len(workflowRuns) == 1