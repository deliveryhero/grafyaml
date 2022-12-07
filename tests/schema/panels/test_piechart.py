import testtools.matchers
from testtools import TestCase

from grafana_dashboards.schema.panel.piechart import PieChart


class TestCasePieChart(TestCase):
    def setUp(self):
        super(TestCasePieChart, self).setUp()
        self.schema = PieChart().get_schema()

    def test_defaults(self):
        defaults = {
            "type": "piechart",
            "title": "test piechart",
            "fieldConfig": {
                "defaults": {},
                "overrides": [],
            },
            "gridPos": {
                "w": 8,
                "h": 8,
                "x": 0,
                "y": 0,
            },
            "options": {},
        }
        self.assertThat(self.schema(defaults), testtools.matchers.Equals(defaults))
