import datetime

from omnim.src.events import EventType
from omnim.src.metrics.change_failure_rate import ChangeFailureRateMetricCalculator
from omnim.src.metrics.leadtime import WorkflowEvent


class TestChangeFailureRateCalculator:
    def test_it_should_return_no_failure_rate_with_no_events(self):
        metric = ChangeFailureRateMetricCalculator()

        result = metric.calculate([])

        assert result.change_failure_rate is None

    def test_should_return_no_failure_rate_with_no_events_of_deploy_success(
        self,
    ):
        metric = ChangeFailureRateMetricCalculator()
        today = datetime.datetime.today()

        deployment_events_stream = (WorkflowEvent(today, EventType.BUILD_SUCCESS),)

        result = metric.calculate(deployment_events_stream)

        assert result.change_failure_rate is None

    def test_should_return_failure_rate_with_of_zero(self):
        metric = ChangeFailureRateMetricCalculator()
        today = datetime.datetime.today()

        deployment_events_stream = (WorkflowEvent(today, EventType.DEPLOY_SUCCESS),)

        result = metric.calculate(deployment_events_stream)

        assert result.change_failure_rate == 0

    def test_it_should_return_failure_rate_of_one(self):
        metric = ChangeFailureRateMetricCalculator()
        today = datetime.datetime.today()

        deployment_events_stream = (
            WorkflowEvent(today, EventType.DEPLOY_SUCCESS),
            WorkflowEvent(
                datetime=today, event_type=EventType.ERROR, data="This is a dummy error"
            ),
        )

        result = metric.calculate(deployment_events_stream)

        assert result.change_failure_rate == 1.0

    def test_it_should_return_failure_rate_of_0_5_for_build_success_followed_by_build_failure(  # noqa: E501
        self,
    ):
        metric = ChangeFailureRateMetricCalculator()
        today = datetime.datetime.today()

        events_stream = (
            WorkflowEvent(today, EventType.DEPLOY_SUCCESS),
            WorkflowEvent(today, EventType.DEPLOY_FAILED),
            WorkflowEvent(today, EventType.DEPLOY_SUCCESS),
            WorkflowEvent(
                datetime=today, event_type=EventType.ERROR, data="This is a dummy error"
            ),
        )

        result = metric.calculate(events_stream)

        assert result.change_failure_rate == 0.5
