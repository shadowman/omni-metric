import csv
from datetime import datetime
import unittest

from metrics.csvloader import CsvEventsLoader

class CsvEventsLoaderTests(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.test_csv_loader = CsvEventsLoader("./data/sample.csv")

    def test_it_should_load_a_parametrized_file(self):
        loader = CsvEventsLoader("test")
        self.assertEqual(loader.file_path, "test")


    def test_it_should_load_each_row_as_a_workflow_event(self):
        self.test_csv_loader.load()

        events = self.test_csv_loader.get_all_events()

        self.assertEqual(len(events), 3)

    def test_it_should_load_each_event_date_and_time_correctly(self):
        self.test_csv_loader.load()

        events = self.test_csv_loader.get_all_events()

        for event in events:
            self.assertEqual(datetime, type(event.datetime))
        
    
    def test_it_should_load_event_names_correctly(self):
        self.test_csv_loader.load()

        events = self.test_csv_loader.get_all_events()

        first_event = events[0]
        self.assertEqual(first_event.name, "build_success")
        
        
    def test_it_should_load_each_event_data_correctly(self):
        self.test_csv_loader.load()

        events = self.loader.get_all_events()

        first_event = events[0]
        self.assertEqual(first_event.data, "pipeline_id1#1")
        
        