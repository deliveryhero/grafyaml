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
            "editable": True,
            "error": False,
            "fieldConfig": {
                "defaults": {},
                "overrides": [],
            },
            "options": {},
        }
        self.assertThat(self.schema(defaults), testtools.matchers.Equals(defaults))
