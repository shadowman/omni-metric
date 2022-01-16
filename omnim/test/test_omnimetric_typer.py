import pytest
from typer.testing import CliRunner

from omnim.src.cli.app import app

runner = CliRunner()


class TestOmniMetricCommandLineAppTyper:

    def test_has_default_help_message(self):
        master_output = ("""Usage: main [OPTIONS]

Options:
  --metrics [lt|df|cfr|mttr]
  --input-file TEXT
""")

        result = runner.invoke(app, ["main", "--help"])

        assert master_output in result.stdout

    def test_should_raise_exception_for_invalid_metric_type(self):
        wrong_metric = "whatever"
        master_output = (
            f"Error: Invalid value for '--metrics': '{wrong_metric}' " 
            f"is not one of 'lt', 'df', 'cfr', 'mttr'"
        )

        result = runner.invoke(app, ["main", "--metrics", wrong_metric])

        assert master_output in result.stdout
