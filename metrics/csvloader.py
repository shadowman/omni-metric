
from metrics.leadtime import WorkflowEvent

class CsvEventsLoader:

    def load(self):
        pass
    def get_all_events(self):
        return [WorkflowEvent(name="build_success", data="pipeline_id1#1"), WorkflowEvent(), WorkflowEvent()]