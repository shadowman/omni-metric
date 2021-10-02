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
        events_stream = (WorkflowEvent(datetime.datetime.today(), "build", "success"),
            WorkflowEvent(datetime.datetime.today() + timedelta(seconds=10),  "deploy", "success"))
        
        result = metric.calculate(events_stream)

        self.assertEqual(timedelta(seconds=10), result)
    