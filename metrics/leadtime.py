import datetime

class LeadtimeMetricCalculator:
    def calculate(self, events = []):
        total_time = datetime.timedelta()
        deploys_count = 0
        pipelines = {}
        for event in events:
            pipeline_execution = pipelines.setdefault(event.data,{"build_time": None, "deploy_time": None})

            if event.name == "build_success":
                pipeline_execution["build_time"] = event.datetime
            if event.name == "deploy_success":
                pipeline_execution["deploy_time"] = event.datetime
                total_time += pipeline_execution["deploy_time"] - pipeline_execution["build_time"]
                deploys_count += 1
        
        average_leadtime = None
        if deploys_count > 0:
            average_leadtime = total_time / deploys_count
        return average_leadtime

class WorkflowEvent:
    def __init__(self, datetime=datetime.datetime.today(), name="event", data=""):
        self.datetime = datetime
        self.name = name
        self.data = data