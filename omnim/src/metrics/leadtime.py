import datetime

from omnim.src.events import EventType
from omnim.src.metrics.metric_result import LeadtimeMetricResult


class LeadtimeMetricCalculator:
    def calculate(self, events=()):
        average_lead_time = None

        total_time = datetime.timedelta()

        deploys_count = 0
        pipelines = {}

        for event in events:
            pipeline_execution = pipelines.setdefault(
                event.data, {"build_time": None, "deploy_time": None}
            )

            if event.type == EventType.BUILD_SUCCESS:
                pipeline_execution["build_time"] = event.datetime
            if (
                event.type == EventType.DEPLOY_SUCCESS
                and pipeline_execution["build_time"] is not None
            ):
                pipeline_execution["deploy_time"] = event.datetime
                total_time += (
                    pipeline_execution["deploy_time"] - pipeline_execution["build_time"]
                )
                deploys_count += 1

        if deploys_count > 0:
            average_lead_time = total_time / deploys_count

        return LeadtimeMetricResult(lead_time=average_lead_time)


class WorkflowEvent:
    def __init__(self, datetime=datetime.datetime.today(), type="null", data=""):
        self.datetime = datetime
        self.type = EventType(type)
        self.data = data
