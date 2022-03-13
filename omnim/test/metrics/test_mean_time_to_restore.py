import datetime

from omnim.src.events import EventType
from omnim.src.metrics.leadtime import WorkflowEvent
from omnim.src.metrics.mean_time_to_restore import \
    MeanTimeToRestoreMetricCalculator


class TestMeanTimeToRestoreMetricCalculator:
    def test_it_should_return_no_mttr_with_no_events(self):

        events = []

        result = MeanTimeToRestoreMetricCalculator().calculate(events)

        assert result.mean_time_to_restore is None

    def test_should_return_mttr_equals_to_none_if_error_does_not_exists(self):
        today = datetime.datetime.today()
        events = [
            WorkflowEvent(today, "deploy_success"),
        ]

        result = MeanTimeToRestoreMetricCalculator().calculate(events)

        assert result.mean_time_to_restore is None

    def test_should_return_mttr_of_one_minute_in_seconds_on_detected_error(
        self,
    ):  # noqa: E501
        today = datetime.datetime.today()
        events = [
            WorkflowEvent(timestamp=today, data="deploy_success"),
            WorkflowEvent(
                timestamp=today + datetime.timedelta(minutes=1),
                event_type=EventType.SERVICE_FAILING,
                data="There has been an error",
            ),
            WorkflowEvent(
                timestamp=today + datetime.timedelta(minutes=2),
                event_type=EventType.SERVICE_RESTORED,
                data="Service is restored",
            ),
        ]

        result = MeanTimeToRestoreMetricCalculator().calculate(events)

        assert result.mean_time_to_restore == 60

    def test_should_take_the_first_error_timestamp_when_detected_service_error_twice(
        self,
    ):  # noqa: E501
        today = datetime.datetime.today()
        events = [
            WorkflowEvent(timestamp=today, data="deploy_success"),
            WorkflowEvent(
                timestamp=today + datetime.timedelta(minutes=1),
                event_type=EventType.SERVICE_FAILING,
                data="There has been an error",
            ),
            WorkflowEvent(
                timestamp=today + datetime.timedelta(minutes=2),
                event_type=EventType.SERVICE_FAILING,
                data="Service is restored",
            ),
            WorkflowEvent(
                timestamp=today + datetime.timedelta(minutes=3),
                event_type=EventType.SERVICE_RESTORED,
                data="Service is restored",
            ),
        ]

        result = MeanTimeToRestoreMetricCalculator().calculate(events)

        assert result.mean_time_to_restore == 120

    def test_should_return_none_if_a_service_is_restored_before_service_failing(
        self,
    ):  # noqa: E501
        today = datetime.datetime.today()
        events = [
            WorkflowEvent(
                timestamp=today + datetime.timedelta(minutes=1),
                event_type=EventType.SERVICE_RESTORED,
                data="There has been an error",
            ),
            WorkflowEvent(
                timestamp=today + datetime.timedelta(minutes=2),
                event_type=EventType.SERVICE_FAILING,
                data="Service is restored",
            ),
        ]

        result = MeanTimeToRestoreMetricCalculator().calculate(events)

        assert result.mean_time_to_restore is None
