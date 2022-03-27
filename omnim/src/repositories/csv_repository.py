import csv
from pathlib import Path
from typing import List

from omnim.src.metrics.leadtime import WorkflowEvent


class CsvRepository:
    field_names: List[str] = ["datetime", "event_name", "data"]

    def __init__(self, target_file: str):
        self.target_file = Path(target_file)

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
                [events_stream.datetime, events_stream.event_type, events_stream.data]
            )
