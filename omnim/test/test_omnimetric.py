import pytest
from omnim.src.omnimetric import (
    OmniMetricCommandLineApp
)
import io
from cli import tests
from cli.app import Abort
from contextlib import redirect_stdout


class TestOmniMetricCommandLineApp(tests.AppTest):
    app_cls = OmniMetricCommandLineApp

    def test_has_default_help_message(self):
        master_output = ("usage: main [-h] [-m METRICS] [-f INPUT_FILE]\n\n"
                "optional arguments:\n"
                "  -h, --help            show this help message and exit\n"
                "  -m METRICS, --metrics METRICS\n" 
                "  -f INPUT_FILE, --input-file INPUT_FILE\n")
        
        s_stdout = io.StringIO()

        with redirect_stdout(s_stdout):
            with self.assertRaises(Abort):
                status, app = self.runapp(self.app_cls, "omni-metric -h")

        self.assertMultiLineEqual(s_stdout.getvalue(), master_output)

    def test_has_lead_time_argument(self):
        status, app = self.runapp(self.app_cls, "omni-metric -m lt")
        self.assertEqual(app.params.metrics,'lt')

    def test_has_deployment_frequency_argument(self):
        status, app = self.runapp(self.app_cls, "omni-metric -m df")
        self.assertEqual(app.params.metrics,'df')
    
    def test_has_input_file_argument(self):
        status, app = self.runapp(self.app_cls, "omni-metric -f ./data/sample.csv")
        self.assertEqual(app.params.input_file,'./data/sample.csv')

class TestOmniMetricCommandLineAppMetricsOutput(tests.AppTest):
    app_cls = OmniMetricCommandLineApp
    
    def test_runs_lead_time_metric_from_csv_file(self):

        master_output = ("Average Build to Deploy Leadtime = 10.0 s\n")
        
        s_stdout = io.StringIO()
        with redirect_stdout(s_stdout):
            status, app = self.runapp(self.app_cls, "omni-metric -m lt -f ./data/sample.csv")
        
        self.assertMultiLineEqual(s_stdout.getvalue(), master_output)

    @pytest.mark.current
    def test_runs_deployment_frequency_metric_from_csv_file(self):

        master_output = ("Average Deployment Frequency = 1.0 dep/day\n")

        s_stdout = io.StringIO()
        with redirect_stdout(s_stdout):
            status, app = self.runapp(self.app_cls, "omni-metric -m df -f ./data/sample.csv")

        self.assertMultiLineEqual(s_stdout.getvalue(), master_output)

if __name__ == '__main__':
    unittest.main()
