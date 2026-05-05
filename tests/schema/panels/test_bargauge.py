import voluptuous as v
from testtools import TestCase

from grafana_dashboards.schema.panel.bargauge import Bargauge


class TestCaseBargauge(TestCase):
    def setUp(self):
        super(TestCaseBargauge, self).setUp()
        self.schema = Bargauge().get_schema()
        self.base = {
            "type": "bargauge",
            "title": "test bargauge",
            "targets": [],
            "options": {"orientation": "auto", "displayMode": "lcd"},
        }

    def test_defaults(self):
        self.schema(self.base)

    def test_datasource_string(self):
        panel = dict(self.base)
        panel["datasource"] = "logistics-inhouse-prom"
        self.schema(panel)

    def test_datasource_dict(self):
        panel = dict(self.base)
        panel["datasource"] = {"uid": "logistics-inhouse-prom", "type": "prometheus"}
        self.schema(panel)
