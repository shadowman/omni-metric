from abc import ABC, abstractmethod
from pydantic import BaseModel

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
    deployment_frequency: float

    def __str__(self) -> str:
        return f"Average Deployment Frequency = {self.deployment_frequency} dep/day"

    def report(self) -> None:
        print(self)
