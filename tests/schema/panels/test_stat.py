from testtools import TestCase

from grafana_dashboards.schema.panel.stat import Stat


class TestCaseStat(TestCase):
    def setUp(self):
        super(TestCaseStat, self).setUp()
        self.schema = Stat().get_schema()

    def test_defaults(self):
        # Ensure default values get parsed correctly.
        defaults = {
            "editable": True,
            "error": False,
            "title": "test",
            "type": "stat",
            "fieldConfig": {
                "defaults": {
                    "color": {"mode": "shades"},
                    "NoneValueMode": "connected",
                    "mappings": [],
                    "unit": "short",
                    "thresholds": {
                        "mode": "absolute",
                        "steps": [{"color": "green", "value": "null"}],
                    },
                },
                "overrides": [],
            },
            "gridPos": {"h": 8, "w": 12, "x": 0, "y": 31},
            "options": {
                "colorMode": "background",
                "graphMode": "none",
                "justifyMode": "auto",
                "orientation": "auto",
                "reduceOptions": {
                    "calcs": ["lastNotNull"],
                    "fields": "",
                    "values": False,
                },
                "textMode": "auto",
            },
            "span": 12,
            "targets": [],
        }
        self.assertEqual(self.schema(defaults), defaults)
