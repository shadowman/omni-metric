import csv
from datetime import datetime
from os.path import exists
from pathlib import Path
from typing import List, Optional

from omnim.src.events import EventType
from omnim.src.metrics.leadtime import WorkflowEvent


class CsvRepository:
    field_names: List[str] = ["datetime", "event_name", "data"]

    def __init__(self, target_file: Path):
        self.target_file = target_file
        self._events: List[WorkflowEvent] = []

    def save(self, events_stream: WorkflowEvent):
        if not self.target_file.is_file():
            with open(self.target_file, "a", newline="") as csvfile:

                writer = csv.DictWriter(csvfile, fieldnames=self.field_names)
                writer.writeheader()

        with open(self.target_file, "a", newline="") as csvfile:
            csv_row_writer = csv.writer(
                csvfile,
                delimiter=",",
                quotechar="|",
                quoting=csv.QUOTE_MINIMAL,
            )
            csv_row_writer.writerow(
                [
                    events_stream.datetime,
                    events_stream.event_type,
                    events_stream.data,
                ]
            )

    def load(self, start: Optional[datetime] = None):
        if not exists(self.target_file):
            raise FileNotFoundError(
                "Please check that the file path provided is correct."
            )

        with open(self.target_file, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                event_datetime = datetime.fromtimestamp(int(row["datetime"]))
                if start is not None and start > event_datetime:
                    continue
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
