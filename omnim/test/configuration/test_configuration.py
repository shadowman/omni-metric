from omnim.src.configuration.config import Config


class TestConfiguration:

    def test_default_configuration_file_should_have_defaul_parameters(self,):

        config = Config()
        assert (
            config.user == "jmaralc"
            and config.repo == "oop_rust"
            and config.deployment_action_name == "Greetings"
        )

    def test_should_load_parameters_from_configuration_file_when_instantiated(self,):
        config_file = "./data/configuration.json"
        config = Config(config_file=config_file)
        assert (
            config.user == "from_json"
            and config.repo == "from_oop_rust"
            and config.deployment_action_name == "from_Greetings"
        )
