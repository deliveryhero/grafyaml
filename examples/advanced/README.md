# Basic example

Export your Grafana API key:

```
export GRAFANA_API_KEY="XXX"
```

Render the templates:

```
/render.py
```

Sync the rendered templates from the `rendered_dashboards` directory:

```
ls rendered_dashboards/*.yaml | xargs -I {} grafana-dashboard --grafana-url https://my-grafana-host.domain.com update "{}"
```
