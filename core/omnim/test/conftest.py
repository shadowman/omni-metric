import json
import os

import pytest
from omnim.src.configuration.config import Config

CSV_FILE_TEST = "./data/stored_from_csv.csv"
CSV_RESULT_FILE = "./data/result.csv"
GITHUB_RESULT_STUB = "./omnim/test/data/github_result.json"


@pytest.fixture
def github_response():
    # Tear up
    with open(GITHUB_RESULT_STUB, "r") as fid:
        github_response = json.load(fid)

    yield github_response

    # Tear down
    if os.path.isfile(CSV_RESULT_FILE):
        os.remove(CSV_RESULT_FILE)


@pytest.fixture
def config():
    return Config()


@pytest.fixture(scope="function")
def csv_environment():
    # Tear up
    yield None

    # Tear down
    if os.path.isfile(CSV_FILE_TEST):
        os.remove(CSV_FILE_TEST)
