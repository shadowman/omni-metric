# omni-metric

The one tool to monitor the 4 key metrics from the accelerate book for your environments

# Diagram

https://miro.com/app/board/uXjVOdNGlQs=/

[![Python CI](https://github.com/shadowman/omni-metric/actions/workflows/delivery.yml/badge.svg)](https://github.com/shadowman/omni-metric/actions/workflows/delivery.yml)

# Docs

We store documentation related to the project under the folder [docs/](./docs/README.md)

# Definitions

- Deployment Frequency: addresses minimizing the batch size in a project (reducing it is a central element of the Lean paradigm). As this is hard to measure in software, they took the deployment frequency of software to production as a proxy.

- Lead Time for Change: defined as “the time it takes to go from code committed to code successfully running in production”. Shorter time is better because it enables faster feedback and course correction as well as the faster delivery of a fix to a defect.

- Time to Restore Service: as failure in rapidly changing complex systems is inevitable the key question for stability is how long it takes to restore service from an incident from the time the incident occurs (e.g., unplanned outage, service impairment)?

- Change Failure Rate: the percentage of changes for the application or service which results in degraded service or subsequently required remediation (e.g., lead to service impairment or outage, require a hot fix, a rollback, a fixforward, or a patch).

# Related projects

- https://github.com/thoughtworks/metrik
- https://github.com/GoogleCloudPlatform/fourkeys
