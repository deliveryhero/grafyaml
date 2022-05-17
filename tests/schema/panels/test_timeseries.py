import testtools.matchers
from testtools import TestCase

from grafana_dashboards.schema.panel.timeseries import Timeseries


class TestCaseTimeseries(TestCase):
    def setUp(self):
        super(TestCaseTimeseries, self).setUp()
        self.schema = Timeseries().get_schema()

    def test_defaults(self):
        defaults = {
            "type": "timeseries",
            "title": "test timeseries",
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
