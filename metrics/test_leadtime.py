from datetime import timedelta
import datetime
import unittest

from metrics.leadtime import LeadtimeMetricCalculator, WorkflowEvent

class LeadTimeCalculatorTests(unittest.TestCase):

    def test_it_should_return_a_timespan(self):
        metric = LeadtimeMetricCalculator()
        
        result = metric.calculate([])

        self.assertEqual(timedelta, type(result))
        
    def test_it_should_return_average_leadtime_of_event_stream(self):
        metric = LeadtimeMetricCalculator()
        today  = datetime.datetime.today()
        events_stream = (WorkflowEvent(today, "build", "success"),
            WorkflowEvent(today + timedelta(seconds=10),  "deploy", "success"))
        
        result = metric.calculate(events_stream)

        self.assertEqual(timedelta(seconds=10), result)
    
    def test_it_should_return_average_leadtime_from_build_to_deploy(self):
        metric = LeadtimeMetricCalculator()
        today  = datetime.datetime.today()
        events_stream = (WorkflowEvent(today, "build", "success"),
            WorkflowEvent(today + timedelta(seconds=10), "test", "success"),
            WorkflowEvent(today + timedelta(seconds=20),  "deploy", "success"))
        
        result = metric.calculate(events_stream)

        self.assertEqual(timedelta(seconds=20), result)

    def test_it_should_not_return_an_average_if_no_deploy_is_found(self):
        metric = LeadtimeMetricCalculator()
        today  = datetime.datetime.today()
        events_stream = (WorkflowEvent(today, "build", "success"),
            WorkflowEvent(today + timedelta(seconds=10), "test", "success"))
        
        result = metric.calculate(events_stream)

        self.assertEqual(timedelta(seconds=0), result)

    def test_it_should_not_return_an_average_if_deploy_is_not_successful(self):
        metric = LeadtimeMetricCalculator()
        today  = datetime.datetime.today()
        events_stream = (WorkflowEvent(today, "build", "success"),
            WorkflowEvent(today + timedelta(seconds=10), "test", "success"),
            WorkflowEvent(today + timedelta(seconds=20),  "deploy", "failed"))

        result = metric.calculate(events_stream)

        self.assertEqual(timedelta(seconds=0), result)

    def test_it_should_not_return_an_average_if_build_is_not_successful(self):
        metric = LeadtimeMetricCalculator()
        today  = datetime.datetime.today()
        events_stream = (WorkflowEvent(today, "build", "failed"),
            WorkflowEvent(today + timedelta(seconds=10), "test", "failed"),
            WorkflowEvent(today + timedelta(seconds=20),  "deploy", "failed"))
            
        result = metric.calculate(events_stream)

        self.assertEqual(timedelta(seconds=0), result)