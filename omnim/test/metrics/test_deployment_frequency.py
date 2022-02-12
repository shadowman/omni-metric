import datetime

from omnim.src.metrics.deployment_frequency import \
    DeploymentFrequencyMetricCalculator
from omnim.src.metrics.leadtime import WorkflowEvent


class TestDeploymentFrequencyCalculator:
    def test_it_should_return_no_frequency_with_no_events(self):

        metric = DeploymentFrequencyMetricCalculator()

        result = metric.calculate([])

        assert result is None

    def test_it_should_return_no_frequency_with_no_deployment_success_event(
        self,
    ):  # noqa: E501

        metric = DeploymentFrequencyMetricCalculator()
        today = datetime.datetime.today()

        events_stream = (WorkflowEvent(today, "build_success"),)

        result = metric.calculate(events_stream)

        assert result is None

    def test_it_should_return_deployment_frequency_of_one(self):

        metric = DeploymentFrequencyMetricCalculator()
        today = datetime.datetime.today()

        events_stream = (
            WorkflowEvent(today, "build_success"),
            WorkflowEvent(today, "deploy_success"),
        )

        result = metric.calculate(events_stream)

        assert result == 1.0

    def test_it_should_return_deployment_frequency_of_0_5(self):

        metric = DeploymentFrequencyMetricCalculator()
        today = datetime.datetime.today()
        yesterday = today - datetime.timedelta(days=2)

        events_stream = (
            WorkflowEvent(yesterday, "build_failed"),
            WorkflowEvent(today, "deploy_success"),
        )

        result = metric.calculate(events_stream)

        assert result == 0.5

    def test_it_should_return_deployment_frequency_of_0_666_for_two_success_deployments_in_3_days(  # noqa: E501
        self,
    ):

        metric = DeploymentFrequencyMetricCalculator()
        today = datetime.datetime.today()
        yesterday = today - datetime.timedelta(days=2)
        day_before = today - datetime.timedelta(days=3)

        events_stream = (
            WorkflowEvent(day_before, "build_failed"),
            WorkflowEvent(yesterday, "build_failed"),
            WorkflowEvent(today, "deploy_success"),
            WorkflowEvent(today, "deploy_success"),
        )

        result = metric.calculate(events_stream)

        assert result == 2 / 3
