from omnim.src.metrics.change_failure_rate import ChangeFailureRateMetricCalculator
from omnim.src.metrics.deployment_frequency import DeploymentFrequencyMetricCalculator
from omnim.src.metrics.leadtime import LeadtimeMetricCalculator
from omnim.src.metrics.mean_time_to_restore import MeanTimeToRestoreMetricCalculator
from omnim.src.metrics.metric_result import MetricResult
from omnim.src.cli.metric import MetricsOptions


def calculate_metrics_for_events(metrics, events):
    available_metrics = {
        MetricsOptions.LEAD_TIME: LeadtimeMetricCalculator,
        MetricsOptions.DEPLOYMENT_FREQUENCY: DeploymentFrequencyMetricCalculator,
        MetricsOptions.CHANGE_FAILURE_RATE: ChangeFailureRateMetricCalculator,
        MetricsOptions.MEAN_TIME_TO_RESTORE: MeanTimeToRestoreMetricCalculator,
    }

    calculator = available_metrics.get(metrics)()

    output: MetricResult = calculator.calculate(events)
    output.report()
