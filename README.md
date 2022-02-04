# grafyaml: Grafana dashboards templated in YAML

[![Delivery Hero ❤️ Grafana](img/banner.png)](#)

[Delivery Hero](https://www.deliveryhero.com/) are big fans of Grafana but when Prometheus becomes your default storage for metrics of all types then the importance of good, consistent and manageable Grafana dashboards becomes paramount. Then once you add many teams, applications, services and environments to the mix, it becomes clear that a tool is needed to manage this complexity. This is that tool 🎉

- No more headaches with copying, pasting and editing JSON
- Template panels and use them in multiple dashboards
- Mass update many dashboards quickly and easily

## Install and quick start

Install `grafyaml`:

```
pip3 install https://github.com/deliveryhero/grafyaml/archive/master.zip
```

Create a file, e.g. `my-example-dashboard.yaml`:

```yaml
dashboard:
  title: My Dashboard
  rows:
  - title: Container metrics
    height: 500px
    panels:
    - title: Container CPU usage
      targets:
      - expr: rate(container_cpu_user_seconds_total[30s]) * 100
      type: graph
```

Sync it to Grafana:

```
export GRAFANA_API_KEY="API_KEY_HERE"
grafana-dashboard --grafana-url https://my-grafana-host.domain.com update my-example-dashboard.yaml
```

## More examples

- [examples/basic](examples/basic): A very basic example with a single dashboard
- [examples/advanced](examples/advanced): An example showing how to create multiple dashboards using templates

## Build and install from source

```
python3 setup.py bdist_wheel
python3 -m pip install --force-reinstall dist/grafyaml-1.0-py3-none-any.whl
```

### Docker
Use the provided docker file to build and test
```
docker build -t grafyaml .

docker run -it --rm -v ${PWD}:/workspace grafyaml bash
```

to build and test you can run the `tox` command




## License, history and contributors

[The LICENSE](LICENSE) is Apache License 2.0. Most of the code in this repository was initially written at [opendev.org/opendev/grafyaml](https://opendev.org/opendev/grafyaml) before being forked to here.
