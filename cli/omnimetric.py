import cli.app

class OmniMetricCommandLineApp(cli.app.CommandLineApp):

    def setup(self):
        super(OmniMetricCommandLineApp, self).setup()
        self.add_param("-m", "--metrics", default=None)
        self.add_param("-f", "--input-file", default=None)

    def main(self):
        pass

if __name__ == "__main__":
    om = OmniMetricCommandLineApp()
    om.run()