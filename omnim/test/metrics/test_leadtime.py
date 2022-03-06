import datetime
import unittest
from datetime import timedelta

from omnim.src.metrics.leadtime import LeadtimeMetricCalculator, WorkflowEvent


class LeadTimeCalculatorTests(unittest.TestCase):
    def test_it_should_return_no_timespan_with_no_events(self):
        metric = LeadtimeMetricCalculator()

        result = metric.calculate([])

        assert result.lead_time is None

    def test_it_should_return_average_leadtime_of_event_stream_in_delta_type(
        self,
    ):  # noqa: E501
        lead_time = timedelta(seconds=10)
        metric = LeadtimeMetricCalculator()
        today = datetime.datetime.today()
        events_stream = (
            WorkflowEvent(today, "build_success"),
            WorkflowEvent(today + lead_time, "deploy_success"),
        )

        result = metric.calculate(events_stream)

        assert result.lead_time == lead_time

    def test_it_should_return_average_leadtime_from_successful_build_to_successful_deploy(  # noqa: E501
        self,
    ):
        expected_result = timedelta(seconds=20)
        metric = LeadtimeMetricCalculator()
        today = datetime.datetime.today()
        events_stream = (
            WorkflowEvent(today, "build_success"),
            WorkflowEvent(today + timedelta(seconds=10), "test_success"),
            WorkflowEvent(today + timedelta(seconds=20), "deploy_success"),
        )

        result = metric.calculate(events_stream)

        assert result.lead_time == expected_result

    def test_it_should_not_return_an_average_if_no_successful_deploy_is_found(
        self,
    ):  # noqa: E501
        metric = LeadtimeMetricCalculator()
        today = datetime.datetime.today()
        events_stream = (
            WorkflowEvent(today, "build_success"),
            WorkflowEvent(today + timedelta(seconds=10), "test_failed"),
        )

        result = metric.calculate(events_stream)

        assert result.lead_time is None

    def test_it_should_not_return_an_average_if_deploy_is_not_successful(self):
        metric = LeadtimeMetricCalculator()
        today = datetime.datetime.today()
        events_stream = (
            WorkflowEvent(today, "build_success"),
            WorkflowEvent(today + timedelta(seconds=10), "test_success"),
            WorkflowEvent(today + timedelta(seconds=20), "deploy_failed"),
        )

        result = metric.calculate(events_stream)

        assert result.lead_time is None


    def test_it_should_not_return_an_average_if_build_is_not_successful(self):
        metric = LeadtimeMetricCalculator()
        today = datetime.datetime.today()
        events_stream = (
            WorkflowEvent(today, "build_failed"),
            WorkflowEvent(today + timedelta(seconds=10), "test_failed"),
            WorkflowEvent(today + timedelta(seconds=20), "deploy_failed"),
        )

        result = metric.calculate(events_stream)

        assert result.lead_time is None

    def test_it_should_not_return_an_average_if_build_is_not_successful_and_deploy_succeeded(  # noqa: E501
        self,
    ):
        metric = LeadtimeMetricCalculator()
        today = datetime.datetime.today()
        events_stream = (
            WorkflowEvent(today, "build_failed"),
            WorkflowEvent(today + timedelta(seconds=10), "test_failed"),
            WorkflowEvent(today + timedelta(seconds=20), "deploy_success"),
        )

        result = metric.calculate(events_stream)

        assert result.lead_time is None

    def test_it_should_return_an_average_if_more_than_one_successful_build(
        self,
    ):  # noqa: E501
        expected_result = timedelta(seconds=25)
        metric = LeadtimeMetricCalculator()
        today = datetime.datetime.today()
        events_stream = (
            WorkflowEvent(today, "build_success"),
            WorkflowEvent(today + timedelta(seconds=20), "deploy_success"),
            WorkflowEvent(today + timedelta(seconds=30), "build_success"),
            WorkflowEvent(today + timedelta(seconds=60), "deploy_success"),
        )

        result = metric.calculate(events_stream)

        assert result.lead_time == expected_result

    def test_it_should_only_look_at_events_from_the_same_pipeline_execution(
        self,
    ):  # noqa: E501
        expected_result = timedelta(seconds=35)
        metric = LeadtimeMetricCalculator()
        today = datetime.datetime.today()
        events_stream = (
            WorkflowEvent(today, "build_success", "pipeline_id1"),
            WorkflowEvent(
                today + timedelta(seconds=30), "build_success", "pipeline_id2"
            ),
            WorkflowEvent(
                today + timedelta(seconds=40), "deploy_success", "pipeline_id1"
            ),
            WorkflowEvent(
                today + timedelta(seconds=60), "deploy_success", "pipeline_id2"
            ),
        )

        result = metric.calculate(events_stream)

        assert result.lead_time == expected_result
