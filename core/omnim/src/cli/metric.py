from enum import Enum


class MetricsOptions(Enum):
    LEAD_TIME = "lt"
    DEPLOYMENT_FREQUENCY = "df"
    CHANGE_FAILURE_RATE = "cfr"
    MEAN_TIME_TO_RESTORE = "mttr"
