#!/usr/bin/env python3
from typing import List
from omnim.src.metrics.leadtime import EventType

class ChangeFailureRateMetricCalculator:

    def __init__(self):
        pass

    def calculate(self, events: List):
        if len(events) == 0:
            return None

        failure_count = 0

        for event in events:
            if event.type == EventType.BUILD_FAILED:
                failure_count += 1

        return  failure_count / len(events)