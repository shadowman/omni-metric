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

    def test_runs_mean_time_to_restore_metric_from_csv_file_and_inform_not_enough_data(self):  # noqa: E501
        master_output = "Not enough data to calculate Mean Time To Restore\n"

        result = self.runner.invoke(
            self.test_app,
            ["--metrics", "mttr", "--input-file", self.data_path]
        )

        assert result.stdout == master_output

    def test_runs_mean_time_to_restore_metric_from_csv_file(self): 
        master_output = "Mean Time To Restore = 60.0 second(s)\n"
        data_path = "./data/mttr_data_stream.csv"

        result = self.runner.invoke(
            self.test_app,
            ["--metrics", "mttr", "--input-file", data_path]
        )

        assert result.stdout == master_output

    def test_load_json_configuration_from_file(self):
        config_file_path = "data/configuration.json"
        data_path = "./data/mttr_data_stream.csv"
        master_output = f"Using '{config_file_path}' as config file"

        result = self.runner.invoke(
            self.test_app,
            ["--config-file", config_file_path, "--metrics", "mttr", "--input-file", data_path]
        )

        assert master_output in result.stdout

    def test_fetch_all_executions_from_github(self):
        config_file_path = "data/configuration.json"
        master_output = "Successfully fetched workflow execution from github\n"

        result = self.runner.invoke(
            self.test_app,
            ["--source", "GitHubActionsForOmnimetric", "--fetch", "", "--config-file", config_file_path]
        )

        assert master_output in result.stdout
