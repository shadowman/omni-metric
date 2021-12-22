from omnim.src.sources.pipeline_source import PipelineSource
from asyncio import sleep
from typing import List, Optional, Dict, Any
import csv


class GithubActionsSource(PipelineSource):

    def __init__(self, user: str, repo: str, ):
        self.user = user
        self.repo = repo
        self.github_url = f"https://api.github.com/repos/{user}/{repo}/actions/runs"
        self.events: List[Optional[str]] = []
        self.pull_period = 10
        self.active = True
        self.target = "result.csv"

    async def listen_source(self):
        while self.active:
            results = await self._pull()

            if results:
                for result in results:
                    await self._register_new_event(result)

        await sleep(self.pull_period)

    async def _pull(self) -> Dict[str, Any]:
        pass

    async def _register_new_event(self, result: Dict):
        with open(self.target, 'w', newline='') as csvfile:
            spamwriter = csv.writer(
                csvfile,
                delimiter=' ',
                quotechar='|',
                quoting=csv.QUOTE_MINIMAL
            )
            spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
            spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
