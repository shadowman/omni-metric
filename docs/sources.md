This is a baisc config for omnimetric sources:

```yml
 sources:
   source:
     name: GitHubActionsForOmnimetric
     type: github
     src:
     API_KEY....
     
     pipelines:
       pipeline:
         name: Python CI
       pipeline:
         name: Python CI

   source:
     name: GitlabForOmnimetrics
     type: gitlab
     src:
     API_KEY....
```

Omni metric needs some kind of state to deal with operations in the
source, here is the current format:

```yml
GitHubActionsForOmnimetric:
  last_sync: 2021-12-01 00:00:01
  key: val
```

Last sync is used to check when to update or fetch new data from the source.

Defined commands for the connectors:

```
omni-metric -c { something: other}") ( I can pass a configuration file )
omni-metric -c config.json ... ") ( I can pass a configuration file )

omni-metric source GitHubActionsForOmnimetric update -date 2021-10-1") ( Bring the latests executions since last sync )
omni-metric source GitHubActionsForOmnimetric fetch") (Bring all executions)
omni-metric source GitHubActionsForOmnimetric ") (default to update action...)
```

# cli > sources_handler > update ... 
