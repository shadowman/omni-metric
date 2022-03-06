from omnim.src.metrics.metric_result import (
    UnknownMetricResult,
    DeployFrequencyMetricResult
)


class TestMetricResult:

    def test_any_metric_should_be_able_to_report_its_current_value(self, capsys):
        # Given
        metric_result = UnknownMetricResult()

        # When
        metric_result.report()

        # Then
        captured = capsys.readouterr()
        assert any(
            "General unspecific metric. No result possible" in c for c in captured
        )

    def test_deployment_frequency_metric_report_the_metric_result_in_human_readeable_format(self, capsys):   # noqa: E501
        # Given
        metric_result = DeployFrequencyMetricResult(**{"deployment_frequency": 10.11})

        # When
        metric_result.report()

        # Then
        captured = capsys.readouterr()
        assert any(
            "Average Deployment Frequency = 10.11 dep/day" in c for c in captured
        )

    def test_deployment_frequency_metric_report_lack_of_information_if_internal_metrics_are_none(self, capsys):   # noqa: E501
        # Given
        metric_result = DeployFrequencyMetricResult(**{"deployment_frequency": None})

        # When
        metric_result.report()

        # Then
        captured = capsys.readouterr()
        assert any(
            "This metric returned an empty value. "
            "It is likely that there was not enough "
            "information to compute it" in c for c in captured
        )
