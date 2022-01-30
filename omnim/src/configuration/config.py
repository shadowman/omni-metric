import json
from typing import Optional


class Config:
    user: str ="jmaralc"
    repo:str ="oop_rust"
    deployment_action_name: str ="Greetings"

    def __init__(self, config_file: Optional[str] = None):
        if config_file is not None:
            with open(config_file, "r") as fid:
                config =json.load(fid)

            self.user = config.get("user")
            self.repo = config.get("repo")
            self.deployment_action_name = config.get("deployment_action_name")