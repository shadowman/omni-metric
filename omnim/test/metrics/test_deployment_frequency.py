import pytest

from omnim.src.metrics.deployment_frequency import DeploymentFrequencyCalculator

@pytest.mark.current
class TestDeploymentFrequencyCalculator:

    def test_it_should_return_no_frequency_with_no_events(self):

        metric = DeploymentFrequencyCalculator()

        result = metric.calculate([])

        assert result is None
