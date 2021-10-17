#!/usr/bin/env python3
from typing import List

class DeploymentFrequencyMetricCalculator:

    def __init__(self):
        pass

    def calculate(self, events: List):
        if len(events) == 0:
            return None

        raise NotImplementedError
