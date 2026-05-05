import voluptuous as v
from testtools import TestCase

from grafana_dashboards.schema.panel.gauge import Gauge


class TestCaseGauge(TestCase):
    def setUp(self):
        super(TestCaseGauge, self).setUp()
        self.schema = Gauge().get_schema()
        self.base = {"type": "gauge", "title": "test gauge", "targets": []}

    def test_defaults(self):
        self.schema(self.base)

    def test_min_max_int(self):
        panel = dict(self.base)
        panel["fieldConfig"] = {"defaults": {"min": 0, "max": 100}, "overrides": []}
        self.schema(panel)

    def test_min_max_float(self):
        panel = dict(self.base)
        panel["fieldConfig"] = {"defaults": {"min": 0.0, "max": 1.0}, "overrides": []}
        self.schema(panel)

    def test_datasource_string(self):
        panel = dict(self.base)
        panel["datasource"] = "logistics-inhouse-prom"
        self.schema(panel)

    def test_datasource_dict(self):
        panel = dict(self.base)
        panel["datasource"] = {"uid": "logistics-inhouse-prom", "type": "prometheus"}
        self.schema(panel)

    def test_min_invalid(self):
        panel = dict(self.base)
        panel["fieldConfig"] = {"defaults": {"min": "not-a-number"}, "overrides": []}
        self.assertRaises(v.Invalid, self.schema, panel)
