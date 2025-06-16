# grafyaml: Grafana dashboards templated in YAML

[![Delivery Hero ❤️ Grafana](img/banner.png)](#)

[Delivery Hero](https://www.deliveryhero.com/) are big fans of Grafana but when Prometheus becomes your default storage for metrics of all types then the importance of good, consistent and manageable Grafana dashboards becomes paramount. Then once you add many teams, applications, services and environments to the mix, it becomes clear that a tool is needed to manage this complexity. This is that tool 🎉

- No more headaches with copying, pasting and editing JSON
- Template panels and use them in multiple dashboards
- Mass update many dashboards quickly and easily

## Install and quick start

Install `grafyaml`:

```console
pip3 install https://github.com/deliveryhero/grafyaml/archive/master.zip
```

Create a file, e.g. `my-example-dashboard.yaml`:

```yaml
dashboard:
  title: My Dashboard
  panels:
  - title: Container metrics
    panels:
    - title: Container CPU usage
      targets:
      - expr: rate(container_cpu_user_seconds_total[30s]) * 100
      type: timeseries
```

Sync it to Grafana:

```console
export GRAFANA_API_KEY="API_KEY_HERE"
grafyaml --grafana-url https://my-grafana-host.domain.com update my-example-dashboard.yaml
```

## Permissions

Grafyaml supports permissions for dashboards. The permissions are defined in the same file as dashboard under `permissions` root key. The permissions are applied to the dashboard as a whole, not to individual panels.

```yaml

permissions:
  strategy: replace # merge or overwrite
  grants:
    # subject:identifier:permission
    - team:admins:admin
dashboard:
  title: My Dashboard
  panels:
  - title: Container metrics
    panels:
    - title: Container CPU usage
      targets:
      - expr: rate(container_cpu_user_seconds_total[30s]) * 100
      type: timeseries
```

Grants are structured as a triplet: `subject:identifier:permission`.

- Subject: Specifies the entity to which the permission applies. Valid subjects include team, user, role, or serviceAccount. (serviceAccount is not yet supported)
- Identifier: The specific name or unique identifier of the subject.
- Permission: Defines the level of access granted. Permissible values are view, edit, admin, or none.

Example: To grant edit permission for the developers team on a resource named my-dashboard, the grant would be defined as team:developers:edit.

## More examples

- [examples/basic](examples/basic): A very basic example with a single dashboard
- **_Timeseries panels_**: [kube_pod.yaml](examples/advanced/templates/kube_pod.yaml): An example of Timeseries panels of kube_pod_* and container_* metrics.
  - An example dashboard: https://dashboards.syslogistics.io/d/FxYFbAXnk/grafyamls-example?orgId=1

## Build and install from source

```
python3 -m pip install wheel
python3 setup.py bdist_wheel
python3 -m pip install --force-reinstall dist/grafyaml-1.0-py3-none-any.whl
```

## How to run linter

This repo uses black as the linter. You can read about it [here](https://black.readthedocs.io/en/stable/getting_started.html)

Install and run linter:

```
pip install black
black .
```

## Release

The release process is automated using Drone CI. See [drone.yml](.drone.yml) for details. We use [semantic-release](https://github.com/semantic-release/semantic-release) for versioning and tagging.To trigger a release create a release PR following the semantic release commit message format.

## License, history and contributors

[The LICENSE](LICENSE) is Apache License 2.0. Most of the code in this repository was initially written at [opendev.org/opendev/grafyaml](https://opendev.org/opendev/grafyaml) before being forked to here.
