#!/bin/bash
rm -rf ./data/result.csv
pipenv run python omnim/src/cli/app.py fetch --source GitHubActionsForOmnimetric --config-file $1
pipenv run python omnim/src/cli/app.py metrics --metrics df --input-file ./data/result.csv