import csv
from datetime import datetime
import unittest

from metrics.csvloader import CsvEventsLoader

class CsvEventsLoaderTests(unittest.TestCase):

    def test_it_should_load_each_row_as_a_workflow_event(self):
        loader = CsvEventsLoader()

        loader.load()

        events = loader.get_all_events()

        self.assertEqual(len(events), 3)

    def test_it_should_load_each_event_date_and_time_correctly(self):
        loader = CsvEventsLoader()

        loader.load()

        events = loader.get_all_events()

        for event in events:
            self.assertEqual(datetime, type(event.datetime))
        
    
    def test_it_should_load_event_names_correctly(self):
        loader = CsvEventsLoader()

        loader.load()

        events = loader.get_all_events()

        first_event = events[0]
        self.assertEqual(first_event.name, "build_success")
        
        
    def test_it_should_load_each_event_data_correctly(self):
        loader = CsvEventsLoader()

        loader.load()

        events = loader.get_all_events()

        first_event = events[0]
        self.assertEqual(first_event.data, "pipeline_id1#1")
        
        