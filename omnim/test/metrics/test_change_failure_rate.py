import datetime

from omnim.src.metrics.change_failure_rate import ChangeFailureRateMetricCalculator
from omnim.src.metrics.leadtime import WorkflowEvent
from omnim.src.events import EventType


class TestChangeFailureRateCalculator:

    def test_it_should_return_no_failure_rate_with_no_events(self):

        metric = ChangeFailureRateMetricCalculator()

        result = metric.calculate([])

        assert result is None


    def test_it_should_return_failure_rate_of_one(self):

        metric = ChangeFailureRateMetricCalculator()
        today = datetime.datetime.today()

        deployment_events_stream = (
            WorkflowEvent(today, "deploy_success"),
            WorkflowEvent(
                datetime=today,
                type=EventType.ERROR,
                data="This is a dummy error"
            ),
        )

        result = metric.calculate(deployment_events_stream)

        assert result == 1.0

    def test_it_should_return_failure_rate_of_0_5_for_build_success_followed_by_build_failure(self):

        metric = ChangeFailureRateMetricCalculator()
        today = datetime.datetime.today()

        events_stream = (
            WorkflowEvent(today, "deploy_success"),
            WorkflowEvent(today, "deploy_failed"),
            WorkflowEvent(today, "deploy_success"),
            WorkflowEvent(
                datetime=today,
                type=EventType.ERROR,
                data="This is a dummy error"
            ),
        )

        result = metric.calculate(events_stream)

        assert result == 0.5
