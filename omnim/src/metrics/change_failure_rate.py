#!/usr/bin/env python3
from typing import List
from omnim.src.metrics.leadtime import EventType
from omnim.src.events.monitor import MonitorEventType
class ChangeFailureRateMetricCalculator:

    def __init__(self):
        pass

    def calculate(self, workflow_events: List, monitoring_events: List):
        if len(workflow_events) == 0:
            return None

        failure_count = 0
        deployment_count = 0

        for event in workflow_events:
            if event.type == EventType.DEPLOY_SUCCESS:
                deployment_count += 1

        for event in monitoring_events:
            if event.type == MonitorEventType.ERROR:
                failure_count += 1

        return  failure_count / deployment_count