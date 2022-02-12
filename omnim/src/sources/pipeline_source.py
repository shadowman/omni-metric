import abc
from typing import Dict


class PipelineSource(abc.ABC):
    @abc.abstractmethod
    def _pull(self):
        raise NotImplementedError("This is still work in progress")

    @abc.abstractmethod
    def listen_source(self):
        raise NotImplementedError("This is still work in progress")

    @abc.abstractmethod
    def _register_new_event(self, result: Dict):
        raise NotImplementedError("This is still work in progress")
