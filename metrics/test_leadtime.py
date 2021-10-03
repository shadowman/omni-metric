from datetime import timedelta
import datetime
import unittest

from metrics.leadtime import LeadtimeMetricCalculator, WorkflowEvent

class LeadTimeCalculatorTests(unittest.TestCase):

    def test_it_should_return_no_timespan_with_no_events(self):
        metric = LeadtimeMetricCalculator()
        
        result = metric.calculate([])

        self.assertEqual(None, result)
        
    def test_it_should_return_average_leadtime_of_event_stream_in_delta_type(self):
        metric = LeadtimeMetricCalculator()
        today  = datetime.datetime.today()
        events_stream = (WorkflowEvent(today, "build_success"),
            WorkflowEvent(today + timedelta(seconds=10),  "deploy_success"))
        
        result = metric.calculate(events_stream)

        self.assertEqual(timedelta(seconds=10), result)
        self.assertEqual(timedelta, type(result))
    
    def test_it_should_return_average_leadtime_from_successful_build_to_successful_deploy(self):
        metric = LeadtimeMetricCalculator()
        today  = datetime.datetime.today()
        events_stream = (WorkflowEvent(today, "build_success"),
            WorkflowEvent(today + timedelta(seconds=10), "test_success"),
            WorkflowEvent(today + timedelta(seconds=20),  "deploy_success"))
        
        result = metric.calculate(events_stream)

        self.assertEqual(timedelta(seconds=20), result)

    def test_it_should_not_return_an_average_if_no_successful_deploy_is_found(self):
        metric = LeadtimeMetricCalculator()
        today  = datetime.datetime.today()
        events_stream = (WorkflowEvent(today, "build_success"),
            WorkflowEvent(today + timedelta(seconds=10), "test_failed"))
        
        result = metric.calculate(events_stream)

        self.assertEqual(None, result)

    def test_it_should_not_return_an_average_if_deploy_is_not_successful(self):
        metric = LeadtimeMetricCalculator()
        today  = datetime.datetime.today()
        events_stream = (WorkflowEvent(today, "build", "success"),
            WorkflowEvent(today + timedelta(seconds=10), "test", "success"),
            WorkflowEvent(today + timedelta(seconds=20),  "deploy", "failed"))

        result = metric.calculate(events_stream)

        self.assertEqual(None, result)

    def test_it_should_not_return_an_average_if_build_is_not_successful(self):
        metric = LeadtimeMetricCalculator()
        today  = datetime.datetime.today()
        events_stream = (WorkflowEvent(today, "build_failed"),
            WorkflowEvent(today + timedelta(seconds=10), "test_failed"),
            WorkflowEvent(today + timedelta(seconds=20),  "deploy_failed"))
            
        result = metric.calculate(events_stream)

        self.assertEqual(None, result)

    def test_it_should_return_an_average_if_more_than_one_successful_build(self):
        metric = LeadtimeMetricCalculator()
        today  = datetime.datetime.today()
        events_stream = (WorkflowEvent(today, "build_success"),
            WorkflowEvent(today + timedelta(seconds=20),  "deploy_success"),
            WorkflowEvent(today + timedelta(seconds=30), "build_success"),
            WorkflowEvent(today + timedelta(seconds=60),  "deploy_success"))
            
        result = metric.calculate(events_stream)

        self.assertEqual(timedelta(seconds=25), result)
    
    def test_it_should_only_look_at_events_from_the_same_pipeline_execution(self):
        metric = LeadtimeMetricCalculator()
        today  = datetime.datetime.today()
        events_stream = (WorkflowEvent(today, "build_success", "pipeline_id1"),
            WorkflowEvent(today + timedelta(seconds=30), "build_success", "pipeline_id2"),
            WorkflowEvent(today + timedelta(seconds=40),  "deploy_success", "pipeline_id1"),
            WorkflowEvent(today + timedelta(seconds=60),  "deploy_success", "pipeline_id2"))
            
        result = metric.calculate(events_stream)

        self.assertEqual(timedelta(seconds=35), result)