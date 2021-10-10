import datetime
from enum import Enum

class EventType(Enum):
    BUILD_SUCCESS = "build_success"
    DEPLOY_SUCCESS = "deploy_success"
    TEST_SUCCESS = "test_success"
    TEST_FAILED = "test_failed"
    BUILD_FAILED = "build_failed"
    DEPLOY_FAILED = "deploy_failed"
    NULL = "null"

class LeadtimeMetricCalculator:
    def calculate(self, events = []):
        total_time = datetime.timedelta()

        deploys_count = 0
        pipelines = {}

        for event in events:
            pipeline_execution = pipelines.setdefault(
                event.data,{"build_time": None, "deploy_time": None}
            )

            if event.type == EventType.BUILD_SUCCESS:
                pipeline_execution["build_time"] = event.datetime
            if (
                event.type == EventType.DEPLOY_SUCCESS and
                pipeline_execution["build_time"] is not None
            ):
                pipeline_execution["deploy_time"] = event.datetime
                total_time += pipeline_execution["deploy_time"] - pipeline_execution["build_time"]
                deploys_count += 1

        average_leadtime = None

        if deploys_count > 0:
            average_leadtime = total_time / deploys_count
        return average_leadtime

class WorkflowEvent:
    def __init__(
        self,
        datetime=datetime.datetime.today(),
        type="null",
        data=""
    ):
        self.datetime = datetime
        self.type = EventType(type)
        self.data = data
