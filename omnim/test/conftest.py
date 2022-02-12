import json
import os

import pytest


@pytest.fixture
def github_response():
    # Tear up
    with open("./omnim/test/data/github_result.json", "r") as fid:
        github_response = json.load(fid)

    yield github_response

    # Tear down
    if os.path.isfile("./data/result.csv"):
        os.remove("./data/result.csv")
