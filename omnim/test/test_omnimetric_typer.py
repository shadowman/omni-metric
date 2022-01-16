import pytest
from typer.testing import CliRunner

from omnim.src.cli.app import app

runner = CliRunner()


class TestOmniMetricCommandLineAppTyper:

    @pytest.mark.current
    def test_has_default_help_message(self):
        master_output = ("""Usage: main [OPTIONS]

Options:
  --metrics TEXT
  --input-file TEXT
""")

        result = runner.invoke(app, ["main", "--help"])

        assert master_output in result.stdout
