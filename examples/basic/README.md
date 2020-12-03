# Basic example

Export your Grafana API key:

```
export GRAFANA_API_KEY="XXX"
```

And sync the YAML file to Grafana:

```
grafana-dashboard --grafana-url https://my-grafana-host.domain.com update dashboard.yaml
```
