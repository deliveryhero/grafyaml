import testtools.matchers
from testtools import TestCase

from grafana_dashboards.schema.panel.statetimeline import StateTimeline


class TestCaseStateTimeline(TestCase):
    def setUp(self):
        super(TestCaseStateTimeline, self).setUp()
        self.schema = StateTimeline().get_schema()

    def test_defaults(self):
        defaults = {
            "type": "state-timeline",
            "title": "test state-timeline",
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
