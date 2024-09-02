import testtools.matchers
from testtools import TestCase

from grafana_dashboards.schema.panel.timeseries import Gauge


class TestCaseGauge(TestCase):
    def setUp(self):
        super(TestCaseGauge, self).setUp()
        self.schema = Gauge().get_schema()

    def test_defaults(self):
        defaults = {
            "type": "gauge",
            "title": "Example Gauge",
            "gridPos": {"h": 9, "w": 12, "x": 0, "y": 0},
            "id": 1,
            "options": {
                "reduceOptions": {
                    "calcs": ["mean"],
                    "fields": "",
                    "values": False,
                    "limit": 100,
                },
                "showThresholdLabels": True,
                "showThresholdMarkers": True,
            },
            "fieldConfig": {
                "defaults": {
                    "min": 0,
                    "max": 100,
                    "unit": "percent",
                    "decimals": 2,
                    "color": {"mode": "palette-classic", "palette": "cool"},
                    "thresholds": {},
                },
                "overrides": [],
            },
            "targets": [],
            "datasource": {"uid": "cgJzmlq7z", "type": "prometheus"},
        }

        self.assertThat(
            self.schema(defaults),
            testtools.matchers.Equals(defaults),
        )
