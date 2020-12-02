# grafyaml: Grafana dashboards templated in YAML

[![Delivery Hero ❤️ Grafana](img/banner.png)](#)

[Delivery Hero](https://www.deliveryhero.com/) are big fans of Grafana, it is used by many teams. When Prometheus becomes your default storage for metrics of all types then the importance of good, consistent and manageable dashboards becomes paramount. Then add many teams, applications, services, environments and it becomes clear that a tool is needed to manage this complexity. This is that tool 🎉

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

```

Sync it to Grafana:

```
export GRAFANA_API_KEY="API_KEY_HERE"

```

## More examples

- [examples/basic](examples/basic): a very basic example with a single dashboard.

## License, history and contributors

[The LICENSE](LICENSE) is Apache License 2.0. Most of the code in this repository was initially written at [opendev.org/opendev/grafyaml](https://opendev.org/opendev/grafyaml) before being forked to here.
