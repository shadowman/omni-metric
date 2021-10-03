import cli.app
from metrics.csvloader import CsvEventsLoader
from metrics.leadtime import LeadtimeMetricCalculator

class OmniMetricCommandLineApp(cli.app.CommandLineApp):

    def setup(self):
        super(OmniMetricCommandLineApp, self).setup()
        self.add_param("-m", "--metrics", default=None)
        self.add_param("-f", "--input-file", default=None)

        self.events_loader = None
        self.events = []

        self.metrics = None

    def main(self):
        if self.params.input_file is not None:
            self.events_loader = CsvEventsLoader(self.params.input_file)
            
        if self.params.metrics == "lt":
            self.metrics = LeadtimeMetricCalculator()
        
        self._load_events()
        self._calculate_metrics()

        return None
    
    def _load_events(self):
        if self.events_loader is not None:
            try:
                self.events_loader.load()
                self.events = self.events_loader.get_all_events()
            except Exception as e:
                raise e
        
    def _calculate_metrics(self):
        if self.metrics is not None:
            try:
                result = self.metrics.calculate(self.events)
            except Exception as e:
                raise e
            if result is not None:
                print("Average Build to Deploy Leadtime =", result.total_seconds(), "s")

            
if __name__ == "__main__":
    om = OmniMetricCommandLineApp()
    om.run()