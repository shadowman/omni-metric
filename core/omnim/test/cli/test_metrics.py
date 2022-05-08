import pytest
from omnim.src.cli.app import app
from typer.testing import CliRunner


@pytest.mark.current
class TestCLIMetricsOutput:
    runner = CliRunner()
    data_path = "./data/sample.csv"

    def test_start_date_and_present_results_taking_data_only_from_that_point(
        self,
    ):
        # Given
        master_output = "Average Deployment Frequency = 0.0 dep/day\n"

        # When
        result = self.runner.invoke(
            app,
            [
                "metrics",
                "--metrics",
                "df",
                "--input-file",
                self.data_path,
                "--start",
                "2022-01-01",
            ],
        )

        # Then
        assert result.stdout == master_output
