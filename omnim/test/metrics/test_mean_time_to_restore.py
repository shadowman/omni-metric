import pytest
import datetime

from omnim.src.metrics.mean_time_to_restore import MeanTimeToRestoreMetricCalculator
from omnim.src.metrics.leadtime import EventType, WorkflowEvent

class TestMeanTimeToRestoreMetricCalculator:

    def test_it_should_return_no__with_no_events(self):

        events = []

        result = MeanTimeToRestoreMetricCalculator().calculate(events)

        assert result is None

    @pytest.mark.current
    def test_should_return_mean_time_to_restore_equals_to_none_if_error_does_not_exists(self):
        today = datetime.datetime.today()
        events = [
            WorkflowEvent(today, "deploy_success"),
        ]

        result = MeanTimeToRestoreMetricCalculator().calculate(events)

        assert result is None

