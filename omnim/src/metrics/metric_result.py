from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Optional


class MetricResult(ABC):

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError("Metric result not implemented yet")

    def report(self) -> None:
        print(self)


class UnknownMetricResult(MetricResult):

    def __str__(self):
        return "General unspecific metric. No result possible"


class DeployFrequencyMetricResult(BaseModel, MetricResult):
    deployment_frequency: Optional[float]

    def __str__(self) -> str:
        if self.deployment_frequency is None:
            return (
                "This metric returned an empty value. "
                "It is likely that there was not enough information to compute it"
            )

        return f"Average Deployment Frequency = {self.deployment_frequency} dep/day"

    def report(self) -> None:
        print(self)
