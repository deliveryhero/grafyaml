import testtools.matchers
from testtools import TestCase

from grafana_dashboards.schema.panel.piechart import PieChart


class TestCasePieChart(TestCase):
    def setUp(self):
        super(TestCasePieChart, self).setUp()
        self.schema = PieChart().get_schema()

    def test_defaults(self):
        defaults = {
            "editable": True,
            "error": False,
            "fieldConfig": {"defaults": {}, "overrides": []},
            "gridPos": {"h": 8, "w": 8, "x": 0, "y": 0},
            "span": 12,
            "targets": [],
            "title": "test piechart",
            "type": "piechart",
        }
        self.assertThat(self.schema(defaults), testtools.matchers.Equals(defaults))
