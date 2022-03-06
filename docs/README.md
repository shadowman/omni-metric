# Introduction

Omni metrics is a tool developed in python to fetch, transform and calculate
the four key metrics defined by the accelerated book. The four key metrics
are the foundation for companies and developers that aim to develop
in a modern and effective way.

# The key four metrics

- Deployment Frequency: addresses minimizing the batch size in a project (reducing it is a central element of the Lean paradigm). As this is hard to measure in software, they took the deployment frequency of software to production as a proxy.

- Lead Time for Change: defined as “the time it takes to go from code committed to code successfully running in production”. Shorter time is better because it enables faster feedback and course correction as well as the faster delivery of a fix to a defect.

- Time to Restore Service: as failure in rapidly changing complex systems is inevitable the key question for stability is how long it takes to restore service from an incident from the time the incident occurs (e.g., unplanned outage, service impairment)?

- Change Failure Rate: the percentage of changes for the application or service which results in degraded service or subsequently required remediation (e.g., lead to service impairment or outage, require a hot fix, a rollback, a fixforward, or a patch).

Omni metrics on one hand, helps developers to keep track of those metrics
automatically. 

## Available sources

In omni, we call sources the different types of font where omni can get data
to operate and calculate the metrics. The following list is defined by the
sources we currently support:

- Github (GitHubActionsForOmnimetric)

## Planned sources

- Gitlab (GitlabCiForOmnimetric)

The source deserves a section for itself as it has it's own details and complexity,
which can be seen [here](./sources.md).

## Configuring omni metrics

By default omni comes without any data to operate on (besides the test data
used for development). In a "common" setting, it would be likely that
you would want to use your own data, for that, the first step
is to configure the source through a JSON file. The following file
is an example of a configuration file that fetches data from the repository
omni-metric.

```json
{
    "user": "shadowman",
    "repo": "omni-metric",
    "deployment_action_name": "Python CI",
    "token": ""
}
```

The `token` can be empty, and it will be required only if the number of requests
exceeds the allowed number, it also depends on the source used.

## Using omni metrics

The first step towards using omni metrics, is to fetch the data required
for calculating the metrics. The first step is to run the following
command (that used the previous configuration file):

```
pipenv run python omnim/src/cli/app.py --source GitHubActionsForOmnimetric --fetch "" --config-file ./config.jso
```

Note: this is using the Github source, see the section [Available sources](#available-sources).

One the command is run, the following message will be displayed:

```
Using 'config.json' as config file
Successfully fetched workflow execution from github
```

### Troubleshooting

TODO