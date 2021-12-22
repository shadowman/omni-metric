from omnim.src.sources.pipeline_source import PipelineSource
from typing import Dict, Any
import csv
import aiohttp
import datetime

ZERO_TIME = datetime.datetime(1970, 1, 1)


class GithubActionsSource(PipelineSource):
    github_date_format: str = "%Y-%m-%dT%H:%M:%SZ"
    github_URI: str = "https://api.github.com"

    def __init__(self, user: str, repo: str, deployment_action_name: str):
        self.user = user
        self.repo = repo
        self.deployment_action_name = deployment_action_name

        self.github_url = (
            f"{self.github_URI}/repos/{user}/{repo}/actions/runs"
        )
        self.target = "result.csv"

    async def listen_source(self):
        results = await self._pull()

        work_flows = results.get("workflow_runs")
        for work_flow in work_flows:
            if work_flow.get("name") != self.deployment_action_name:
                continue
            conclusion = work_flow.get("conclusion")
            created_at = work_flow.get("created_at")
            created_at = datetime.datetime.strptime(
                created_at,
                self.github_date_format
            )
            timestamp = int(
                (created_at - ZERO_TIME) / datetime.timedelta(seconds=1)
            )
            event = {
                "timestamp": timestamp,
                "event_name": conclusion,
            }
            await self._register_new_event(event)

    async def _pull(self) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.github_url) as response:
                if response.status:
                    result = await response.json()
                else:
                    raise Exception(
                        f"Github issue, response with {response.status}"
                    )
        return result

    async def _register_new_event(self, result: Dict):
        with open(self.target, 'a', newline='') as csvfile:
            csv_row_writer = csv.writer(
                csvfile,
                delimiter=',',
                quotechar='|',
                quoting=csv.QUOTE_MINIMAL
            )
            csv_row_writer.writerow(result.values())
