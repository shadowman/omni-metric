import pytest
from typer.testing import CliRunner

from omnim.src.cli.app import app


@pytest.mark.current
class TestOmniMetricTyperMetricsOutput:

    runner = CliRunner()
    test_app = app
    data_path = "./data/sample.csv"

    def test_runs_lead_time_metric_from_csv_file(self):

        master_output = "Average Build to Deploy Leadtime = 10.0 s\n"

        result = self.runner.invoke(
            self.test_app,
            ["--metrics", "lt", "--input-file", self.data_path]
        )

        assert result.stdout == master_output

    def test_runs_deployment_frequency_metric_from_csv_file(self):

        master_output = "Average Deployment Frequency = 1.0 dep/day\n"

        result = self.runner.invoke(
            self.test_app,
            ["--metrics", "df", "--input-file", self.data_path]
        )

        assert result.stdout == master_output

    def test_runs_change_failure_rate_metric_from_csv_file(self):
        master_output = "Average Change Failure Rate = 0.0 failures/dep\n"

        result = self.runner.invoke(
            self.test_app,
            ["--metrics", "cfr", "--input-file", self.data_path]
        )

        assert result.stdout == master_output

    @pytest.mark.skip
    def test_runs_mean_time_to_restore_metric_from_csv_file_and_inform_not_enough_data(self):  # noqa: E501
        pass

    @pytest.mark.skip
    def test_runs_mean_time_to_restore_metric_from_csv_file(self): 
        pass