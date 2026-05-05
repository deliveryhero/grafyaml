import voluptuous as v
from testtools import TestCase

from grafana_dashboards.schema.panel.logs import Logs


class TestCaseLogs(TestCase):
    def setUp(self):
        super(TestCaseLogs, self).setUp()
        self.schema = Logs().get_schema()
        self.base = {"type": "logs", "title": "test logs", "targets": []}

    def test_defaults(self):
        self.schema(self.base)

    def test_dedup_strategy_values(self):
        for value in ("none", "exact", "numbers", "signature"):
            panel = dict(self.base)
            panel["options"] = {"dedupStrategy": value}
            self.schema(panel)

    def test_dedup_strategy_invalid(self):
        panel = dict(self.base)
        panel["options"] = {"dedupStrategy": "invalid"}
        self.assertRaises(v.Invalid, self.schema, panel)

    def test_sort_order_values(self):
        for value in ("Ascending", "Descending"):
            panel = dict(self.base)
            panel["options"] = {"sortOrder": value}
            self.schema(panel)

    def test_sort_order_invalid(self):
        panel = dict(self.base)
        panel["options"] = {"sortOrder": "invalid"}
        self.assertRaises(v.Invalid, self.schema, panel)

    def test_datasource_string(self):
        panel = dict(self.base)
        panel["datasource"] = "logistics-inhouse-prom"
        self.schema(panel)

    def test_datasource_dict(self):
        panel = dict(self.base)
        panel["datasource"] = {"uid": "logistics-inhouse-prom", "type": "prometheus"}
        self.schema(panel)
