from typing import List

from omnim.src.events import EventType
from omnim.src.metrics.metric_result import MeanTimeToRestoreMetricResult


class MeanTimeToRestoreMetricCalculator:
    def __init__(self):
        pass

    def calculate(self, workflow_events: List) -> MeanTimeToRestoreMetricResult:
        mean_time_to_restore = None

        times_to_restore = []
        last_error_timestamp = None

        for event in workflow_events:
            if (
                event.event_type == EventType.SERVICE_FAILING
                and last_error_timestamp is None
            ):
                last_error_timestamp = event.datetime
            if (
                event.event_type == EventType.SERVICE_RESTORED
                and last_error_timestamp is not None
            ):
                times_to_restore.append(
                    (event.datetime - last_error_timestamp).total_seconds()
                )
                last_error_timestamp = None

        if len(times_to_restore) > 0:
            mean_time_to_restore = sum(times_to_restore) / len(times_to_restore)

        return MeanTimeToRestoreMetricResult(mean_time_to_restore=mean_time_to_restore)
