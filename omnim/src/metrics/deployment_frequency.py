#!/usr/bin/env python3
from typing import List
from omnim.src.metrics.leadtime import EventType

class DeploymentFrequencyMetricCalculator:

    def __init__(self):
        pass

    def calculate(self, events: List):
        if len(events) == 0:
            return None

        deployment_frequency = None
        deploys_count = 0

        event_start_date = events[0].datetime
        event_end_date = events[len(events) - 1].datetime

        elapsed_time = event_end_date - event_start_date

        for event in events:
            if event.type == EventType.DEPLOY_SUCCESS:
                deploys_count += 1

        days = elapsed_time.days

        if days == 0:
            days = 1

        deployment_frequency = deploys_count / days

        if deployment_frequency == 0:
            return None

        if deployment_frequency < 1:
            return deployment_frequency

        return int(deployment_frequency)
