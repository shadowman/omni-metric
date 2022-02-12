class OmniMetricException(Exception):
    pass


class TokenNotFoundException(OmniMetricException):
    def __init__(self, message="Not token provided!"):
        self.message = message
        super().__init__(self.message)
