import pytest
import io
from contextlib import redirect_stdout
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
