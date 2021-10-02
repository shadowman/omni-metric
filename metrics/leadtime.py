import datetime

class LeadtimeMetricCalculator:
    def calculate(self, events = []):
        return datetime.timedelta(seconds=10)

class WorkflowEvent:
    def __init__(self, moment, name, data):
        self.moment = moment
        self.name = name
        self.data = data