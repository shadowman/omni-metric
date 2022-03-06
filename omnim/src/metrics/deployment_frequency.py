#!/usr/bin/env python3
from typing import List

from omnim.src.events import EventType
from omnim.src.metrics.metric_result import DeployFrequencyMetricResult


class DeploymentFrequencyMetricCalculator:
    def __init__(self):
        pass

    def calculate(self, events: List):
        deployment_frequency = None

        if len(events) == 0:
            return DeployFrequencyMetricResult(
                deployment_frequency=deployment_frequency
            )

        deploys_count = 0

        for event in events:
            if event.type == EventType.DEPLOY_SUCCESS:
                deploys_count += 1
        if deploys_count > 0:
            event_start_date = events[0].datetime
            event_end_date = events[len(events) - 1].datetime
            elapsed_time = event_end_date - event_start_date
            days = elapsed_time.days if elapsed_time.days > 0 else 1
            deployment_frequency = deploys_count / days

        return DeployFrequencyMetricResult(deployment_frequency=deployment_frequency)
