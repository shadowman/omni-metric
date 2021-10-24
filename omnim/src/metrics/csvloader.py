
import csv
import datetime
from os.path import exists


from omnim.src.metrics.leadtime import WorkflowEvent

class CsvEventsLoader:
    def __init__(self, file = None) -> None:
        self.file_path = file

    def load(self):
        if not exists(self.file_path):
            raise FileNotFoundError("Please check that the file path provided is correct.")
        
        self._events = []

        with open(self.file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                event_datetime = datetime.datetime.fromtimestamp(int(row["datetime"]))
                event_name = row["event_name"]
                event_data = row["data"]
                
                event = WorkflowEvent(event_datetime, event_name, event_data)

                self._events.append(event)

    def get_all_events(self):
        return self._events

# Workflow
# class GithubEventsLoader
# class GitlabEventsloader

# Monitoring
# class NewRelicEventsLoader
# class PrometheusEventsLoader

