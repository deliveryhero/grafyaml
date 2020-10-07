# Grafyaml

Free software: Apache license

Forked from [Grafyaml](https://opendev.org/opendev/grafyaml). This fork adds support for new panel types like log panel, stat panel etc. and also adds other features like annotations and constant template type.


### Introduction

grafyaml helps you create Grafana dashboards in code using YAML format.

### Installation

Install using pip: `pip3 install git+https://github.com/deliveryhero/grafyaml.git`


### How To Use

1. Create a dashboard yaml file using the yaml specified below.

```yaml
dashboard:
  editable: false
  annotations:
    list:
    - datasource: $datasource
      enable: true
      expr: query_for_my_annotation
      hide: false
      name: My Annotation
  templating:
  - current:
      text: DatasourceName
      value: DatasourceName
    label: Datasource
    name: datasource
    query: prometheus
    type: datasource
  rows:
  - collapse: false
    height: 300px
    panels:
    - datasource: $datasource
      fill: 8
      span: 4
      targets:
      - expr: rate(container_cpu_user_seconds_total[30s]) * 100
      title: CPU Utilisation
      type: graph
```

3. Validate the dashboard for any issues:

`grafana-dashboard --grafana-url https://localhost:3000 --grafana-folderid <GRAFANA_FOLDER_ID> --grafana-apikey <YOUR_GRAFANA_API_TOKEN_HERE> validate <PATH TO DASHBOARD YAML FILE>`

2. Sync the dashboard to your Grafana:

`grafana-dashboard --grafana-url https://localhost:3000 --grafana-folderid <GRAFANA_FOLDER_ID> --grafana-apikey <YOUR_GRAFANA_API_TOKEN_HERE> update <PATH TO DASHBOARD YAML FILE>`

And that's it you should see your dashboard created on Grafana.
