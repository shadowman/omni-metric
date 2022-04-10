import csv
import datetime
from pathlib import Path
from typing import Any, Dict, List

import aiohttp
from omnim.src.configuration.config import Config
from omnim.src.exceptions.exceptions import TokenNotFoundException
from omnim.src.sources.pipeline_source import PipelineSource

ZERO_TIME = datetime.datetime(1970, 1, 1)

# TODO: just the idea of using pydantic something like
# class GithubActionsEvents(BaseModel):
#     timestamp: datetime
#     event_name: EventType
#     data: str


class GithubActionsSource(PipelineSource):
    github_date_format: str = "%Y-%m-%dT%H:%M:%SZ"
    github_URI: str = "https://api.github.com"
    field_names: List[str] = ["datetime", "event_name", "data"]
    github_events = {
        "success": "deploy_success",
        "failure": "deploy_failed",
    }
    user: str
    repo: str
    deployment_action_name: str
    token: str
    github_url: str
    target: Path

    def __init__(self, config: Config, target: Path):
        self.configure(
            config.user,
            config.token,
            config.repo,
            config.deployment_action_name,
        )
        self.target = target

    def configure(
        self,
        user: str,
        token: str,
        repo: str,
        deployment_action_name: str,
    ):
        self.user = user
        self.repo = repo
        self.deployment_action_name = deployment_action_name

        if not token:
            raise TokenNotFoundException()
        self.token = token

        self.github_url = f"{self.github_URI}/repos/{user}/{repo}/actions/runs"

    async def listen_source(self):
        results = await self._pull()

        work_flows = results.get("workflow_runs")
        if work_flows is not None:
            for work_flow in work_flows:
                if work_flow.get("name") != self.deployment_action_name:
                    continue
                conclusion = work_flow.get("conclusion")

                created_at = work_flow.get("created_at")
                created_at = datetime.datetime.strptime(
                    created_at,
                    self.github_date_format,
                )
                timestamp = int(
                    (created_at - ZERO_TIME) / datetime.timedelta(seconds=1)
                )

                await self._register_new_event(
                    {
                        "timestamp": timestamp,
                        "event_name": self.github_events.get(conclusion, "null"),
                        "data": self.repo,
                    }
                )

    async def _pull(self) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.github_url) as response:
                if response.status:
                    result = await response.json()
                else:
                    raise Exception(f"Github issue, response with {response.status}")
        return result

    async def _register_new_event(self, result: Dict):
        if not self.target.is_file():
            with open(self.target, "a", newline="") as csvfile:

                writer = csv.DictWriter(csvfile, fieldnames=self.field_names)
                writer.writeheader()

        with open(self.target, "a", newline="") as csvfile:
            csv_row_writer = csv.writer(
                csvfile,
                delimiter=",",
                quotechar="|",
                quoting=csv.QUOTE_MINIMAL,
            )
            csv_row_writer.writerow(result.values())
