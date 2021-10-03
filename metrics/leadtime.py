import datetime

class LeadtimeMetricCalculator:
    def calculate(self, events = []):
        total_time = datetime.timedelta()
        deploys_count = 0
        for event in events:
            if event.name == "build":
                start_time = event.datetime
            if event.name == "deploy":
                end_time = event.datetime
                total_time += end_time - start_time
                deploys_count += 1
        
        average_leadtime = datetime.timedelta()
        if deploys_count > 0:
            average_leadtime = total_time / deploys_count
        return average_leadtime

class WorkflowEvent:
    def __init__(self, datetime, name, data):
        self.datetime = datetime
        self.name = name
        self.data = data