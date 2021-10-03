
import csv
import datetime

from metrics.leadtime import WorkflowEvent

class CsvEventsLoader:
    def __init__(self, file = None) -> None:
        self.file = file

    def load(self):
        if self.file == None:
            raise FileNotFoundError()
        
        self._events = []

        with open(self.file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                event_datetime = datetime.datetime.fromtimestamp(int(row["datetime"]))
                event_name = row["event_name"]
                event_data = row["data"]
                
                event = WorkflowEvent(event_datetime, event_name, event_data)

                self._events.append(event)

    def get_all_events(self):
        return self._events