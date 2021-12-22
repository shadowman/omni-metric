import os
import pytest
import json


@pytest.fixture
def github_response():
    # Tear up
    with open("./omnim/test/data/github_result.json", "r") as fid:
        github_response = json.load(fid)

    yield github_response

    # Tear down
    if os.path.isfile("result.csv"):
        os.remove("result.csv")
