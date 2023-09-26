import testtools.matchers
from testtools import TestCase

from grafana_dashboards.schema.panel.timeseries import Bargauge


class TestCaseBargauge(TestCase):
    def setUp(self):
        super(TestCaseBargauge, self).setUp()
        self.schema = Bargauge().get_schema()

    def test_defaults(self):
        defaults = {
            "type": "bargauge",
            "title": "test bargauge",
            "fieldConfig": {
                "defaults": {
                    "thresholds": {
                        "mode": "absolute",
                        "steps": {{"color": "green", "value": "null"}},
                    },
                    "mappings": [],
                },
                "overrides": [],
                "color": {"mode": "palette-classic"},
                "noValue": "0",
                "unit": "none",
            },
            "gridPos": {
                "w": 8,
                "h": 8,
                "x": 0,
                "y": 0,
            },
            "options": {},
        }
        self.assertThat(
            self.schema(defaults),
            testtools.matchers.Equals(defaults),
        )
