import datetime
from typing import Dict, Optional

from omnim.src.events import EventType
from omnim.src.metrics.metric_result import LeadtimeMetricResult


class LeadtimeMetricCalculator:
    def calculate(self, events=()) -> LeadtimeMetricResult:
        average_lead_time = None

        total_time = datetime.timedelta()

        deploys_count = 0
        pipelines: Dict[str, Dict[str, Optional[datetime.datetime]]] = {}

        for event in events:
            pipeline_execution = pipelines.setdefault(event.data, {"build_time": None})

            if event.type == EventType.BUILD_SUCCESS:
                pipeline_execution["build_time"] = event.datetime
            if (
                event.type == EventType.DEPLOY_SUCCESS
                and pipeline_execution.get("build_time") is not None
            ):
                total_time += event.datetime - pipeline_execution.get("build_time")
                deploys_count += 1

        if deploys_count > 0:
            average_lead_time = total_time / deploys_count

        return LeadtimeMetricResult(lead_time=average_lead_time)


class WorkflowEvent:
    def __init__(
        self,
        timestamp=datetime.datetime.today(),
        event_type="null",
        data="",
    ):
        self.datetime = timestamp
        self.type = EventType(event_type)
        self.data = data
