from enum import Enum
import datetime

class MonitorEventType(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class MonitorEvent:

    def __init__(
        self,
        datetime=datetime.datetime.today(),
        type = MonitorEventType.INFO,
        data=""
    ):
        self.datetime = datetime
        self.type = MonitorEventType(type)
        self.data = data
