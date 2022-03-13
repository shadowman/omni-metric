#!/usr/bin/env python3
from typing import List

from omnim.src.events import EventType
from omnim.src.metrics.metric_result import ChangeFailureRateMetricResult


class ChangeFailureRateMetricCalculator:
    def __init__(self):
        pass

    def calculate(self, workflow_events: List) -> ChangeFailureRateMetricResult:
        change_failure_rate = None

        if len(workflow_events) == 0:
            return ChangeFailureRateMetricResult(
                change_failure_rate=change_failure_rate
            )

        failure_count = 0
        deployment_count = 0

        for event in workflow_events:
            if event.type == EventType.DEPLOY_SUCCESS:
                deployment_count += 1
            if event.type == EventType.ERROR:
                failure_count += 1

        if deployment_count == 0:
            change_failure_rate = None
        else:
            change_failure_rate = failure_count / deployment_count

        return ChangeFailureRateMetricResult(change_failure_rate=change_failure_rate)
