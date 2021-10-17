import datetime
import pytest

from omnim.src.metrics.deployment_frequency import DeploymentFrequencyMetricCalculator
from omnim.src.metrics.leadtime import WorkflowEvent

@pytest.mark.current
class TestDeploymentFrequencyCalculator:

    def test_it_should_return_no_frequency_with_no_events(self):

        metric = DeploymentFrequencyMetricCalculator()

        result = metric.calculate([])

        assert result is None

    def test_it_should_return_no_frequency_with_no_deployment_success_event(self):

        metric = DeploymentFrequencyMetricCalculator()
        today  = datetime.datetime.today()

        events_stream = (
            WorkflowEvent(today, "build_success"),
        )

        result = metric.calculate(events_stream)

        assert result is None

    def test_it_should_return_deployment_frequency_of_one(self):

        metric = DeploymentFrequencyMetricCalculator()
        today  = datetime.datetime.today()

        events_stream = (
            WorkflowEvent(today, "build_success"),
            WorkflowEvent(today, "deploy_success"),
        )

        result = metric.calculate(events_stream)

        assert result == 1.0

    def test_it_should_return_deployment_frequency_of_0_5(self):

        metric = DeploymentFrequencyMetricCalculator()
        today  = datetime.datetime.today()
        yesterday  = today - datetime.timedelta(days=2)

        events_stream = (
            WorkflowEvent(yesterday, "build_failed"),
            WorkflowEvent(today, "deploy_success"),
        )

        result = metric.calculate(events_stream)

        assert result == 0.5
