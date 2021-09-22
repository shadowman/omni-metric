
import omnimetric

from cli import tests

class TestOmniMetricCommandLineApp(tests.AppTest):
    app_cls = omnimetric.OmniMetricCommandLineApp
    
    def test_has_lead_time_argument(self):
        status, app = self.runapp(self.app_cls, "omni-metric -m lt")
        self.assertEqual(app.params.metrics,'lt')
    
    def test_has_input_file_argument(self):
        status, app = self.runapp(self.app_cls, "omni-metric -f input.csv")
        self.assertEqual(app.params.input_file,'input.csv')

if __name__ == '__main__':
    unittest.main()