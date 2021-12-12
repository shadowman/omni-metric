class GithubPullActionsRun:

    def __init__(self, settings, github_api_response):
        self.settings = settings
        self.github_api_response = github_api_response

    def pull(self):
        runs = []
        workflowKey = "workflow_runs"

        if workflowKey in self.github_api_response and len(self.github_api_response[workflowKey]) > 0:
            for run in self.github_api_response[workflowKey]:
                if run["head_branch"] == self.settings["branch"]:
                    runs.append("apple")

        return runs