import csv
import unittest

from metrics.csvloader import CsvEventsLoader

class CsvEventsLoaderTests(unittest.TestCase):

    def test_it_should_load_each_row_as_a_workflow_event(self):
        loader = CsvEventsLoader()

        loader.load()

        events = loader.get_all_events()

        self.assertEqual(len(events), 3)

    def test_it_should_load_each_event_date_and_time_correctly(self):
        self.fail()
        
    
    def test_it_should_load_each_event_name_correctly(self):
        self.fail()
        
    def test_it_should_load_each_event_data_correctly(self):
        self.fail()
        