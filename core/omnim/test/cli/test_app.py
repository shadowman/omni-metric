from unittest.mock import patch

import pytest
from omnim.src.cli.app import app
from typer.testing import CliRunner


class TestOmniMetricTyperMetricsOutput:

    runner = CliRunner()
    data_path = "./data/sample.csv"
    config_path = "./data/configuration.json"

    def test_runs_lead_time_metric_from_csv_file(self):

        master_output = "Average Build to Deploy Leadtime = 10.0 s\n"

        result = self.runner.invoke(
            app, ["metrics", "--metrics", "lt", "--input-file", self.data_path]
        )

        assert result.stdout == master_output

    def test_runs_deployment_frequency_metric_from_csv_file(self):

        master_output = "Average Deployment Frequency = 1.0 dep/day\n"

        result = self.runner.invoke(
            app, ["metrics", "--metrics", "df", "--input-file", self.data_path]
        )

        assert result.stdout == master_output

    def test_runs_change_failure_rate_metric_from_csv_file(self):
        master_output = "Average Change Failure Rate = 0.0 failures/dep\n"

        result = self.runner.invoke(
            app,
            [
                "metrics",
                "--metrics",
                "cfr",
                "--input-file",
                self.data_path,
            ],
        )

        assert result.stdout == master_output

    def test_runs_mean_time_to_restore_metric_from_csv_file_and_inform_not_enough_data(  # noqa: E501
        self,
    ):  # noqa: E501
        master_output = (
            "This metric returned an empty value. "
            "It is likely that there was not enough "
            "information to compute it\n"
        )

        result = self.runner.invoke(
            app,
            [
                "metrics",
                "--metrics",
                "mttr",
                "--input-file",
                self.data_path,
            ],
        )

        assert result.stdout == master_output

    def test_runs_mean_time_to_restore_metric_from_csv_file(self):
        master_output = "Mean Time To Restore = 60.0 second(s)\n"
        data_path = "./data/mttr_data_stream.csv"

        result = self.runner.invoke(
            app, ["metrics", "--metrics", "mttr", "--input-file", data_path]
        )

        assert result.stdout == master_output

    def test_load_json_configuration_from_file(self):
        config_file_path = "data/configuration.json"
        data_path = "./data/mttr_data_stream.csv"
        master_output = f"Using '{config_file_path}' as config file"

        result = self.runner.invoke(
            app,
            [
                "fetch",
                "--config-file",
                config_file_path,
                "--input-file",
                data_path,
            ],
        )

        assert master_output in result.stdout

    def test_load_json_configuration_from_file_should_show_storage_type(self):
        config_file_path = "data/configuration.json"
        data_path = "./data/mttr_data_stream.csv"
        expected_storage = "csv"
        master_output = f"Configuration set to use: {expected_storage} storage"

        result = self.runner.invoke(
            app,
            [
                "fetch",
                "--config-file",
                config_file_path,
                "--input-file",
                data_path,
            ],
        )

        assert master_output in result.stdout

    def test_fetch_all_executions_from_github(self):
        config_file_path = "data/configuration.json"
        master_output = "Successfully fetched workflow execution from github\n"

        result = self.runner.invoke(
            app,
            [
                "fetch",
                "--source",
                "GitHubActionsForOmnimetric",
                "--config-file",
                config_file_path,
                "--input-file",
                self.data_path,
            ],
        )
        assert master_output in result.stdout

    @pytest.mark.skip(
        "this test is not supported anymore, it does too many things"
    )  # noqa: E501
    def test_runs_deployment_frequency_metric_from_source_when_configuration_for_that_source_is_provided(  # noqa: E501
        self, github_response
    ):

        with patch(
            "omnim.src.sources.github_actions.GithubActionsSource._pull",
            return_value=github_response,
        ):
            master_output = "Average Deployment Frequency = 2.0 dep/day\n"

            result = self.runner.invoke(
                app,
                [
                    "metrics",
                    "--metrics",
                    "df",
                    "--config-file",
                    self.config_path,
                    "--source",
                    "github",
                ],
            )

            assert master_output in result.stdout

    @pytest.mark.skip
    def test_has_default_help_message_without_arguments(self):
        master_output = """Usage: root metrics [OPTIONS]

Options:
  --config-file PATH
  --metrics [lt|df|cfr|mttr]
  --input-file PATH
  --source TEXT
  --fetch TEXT"""

        result = self.runner.invoke(app)

        assert master_output in result.stdout
