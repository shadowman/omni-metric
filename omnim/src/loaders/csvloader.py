import csv
import datetime
from os.path import exists
from typing import List

from omnim.src.events import EventType
from omnim.src.metrics.leadtime import WorkflowEvent


class CsvEventsLoader:
    def __init__(self, file=None) -> None:
        self.file_path = file
        self._events: List[WorkflowEvent] = []

    def load(self):
        if not exists(self.file_path):
            raise FileNotFoundError(
                "Please check that the file path provided is correct."
            )

        with open(self.file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                event_datetime = datetime.datetime.fromtimestamp(int(row["datetime"]))
                event_name = row["event_name"]
                event_data = row["data"]

                event = WorkflowEvent(
                    datetime=event_datetime,
                    event_type=EventType(event_name),
                    data=event_data,
                )

                self._events.append(event)

    def get_all_events(self) -> List[WorkflowEvent]:
        return self._events


# Workflow
# class GithubEventsLoader
# class GitlabEventsloader

# Monitoring
# class NewRelicEventsLoader
# class PrometheusEventsLoader
