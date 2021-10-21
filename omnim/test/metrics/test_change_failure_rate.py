import datetime
import pytest

from omnim.src.metrics.change_failure_rate import ChangeFailureRateMetricCalculator
from omnim.src.metrics.leadtime import WorkflowEvent

class TestChangeFailureRateCalculator:

    def test_it_should_return_no_failure_rate_with_no_events(self):

        metric = ChangeFailureRateMetricCalculator()

        result = metric.calculate([])

        assert result is None

    def test_it_should_return_failure_rate_of_one(self):

        metric = ChangeFailureRateMetricCalculator()
        today  = datetime.datetime.today()

        events_stream = (
            WorkflowEvent(today, "build_failed"),
        )

        result = metric.calculate(events_stream)
        assert result == 1.0


    def test_it_should_return_failure_rate_of_0_5_for_build_success_followed_by_build_failure(self):

        metric = ChangeFailureRateMetricCalculator()
        today  = datetime.datetime.today()

        events_stream = (
            WorkflowEvent(today, "build_success"),
            WorkflowEvent(today, "build_failed"),
        )

        result = metric.calculate(events_stream)
        assert result == 0.5

