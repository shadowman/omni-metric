from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Optional

from omnim.src.events import EventType
from omnim.src.metrics.metric_result import LeadtimeMetricResult


class LeadtimeMetricCalculator:
    def calculate(self, events=()) -> LeadtimeMetricResult:
        average_lead_time = None

        total_time = timedelta()

        deploys_count = 0
        pipelines: Dict[str, Dict[str, Optional[datetime]]] = {}

        for event in events:
            pipeline_execution = pipelines.setdefault(event.data, {"build_time": None})

            if event.event_type == EventType.BUILD_SUCCESS:
                pipeline_execution["build_time"] = event.datetime
            if (
                event.event_type == EventType.DEPLOY_SUCCESS
                and pipeline_execution.get("build_time") is not None
            ):
                total_time += event.datetime - pipeline_execution.get("build_time")
                deploys_count += 1

        if deploys_count > 0:
            average_lead_time = total_time / deploys_count

        return LeadtimeMetricResult(lead_time=average_lead_time)


@dataclass
class WorkflowEvent:
    datetime: datetime = datetime.today()
    event_type: EventType = EventType("null")
    data: str = ""

    # def __init__(
    #     self,
    #     datetime=datetime.datetime.today(),
    #     event_type="null",
    #     data="",
    # ):
    #     self.datetime = timestamp
    #     self.type = EventType(event_type)
    #     self.data = data
