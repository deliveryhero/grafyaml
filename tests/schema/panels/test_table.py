from testtools import TestCase

from grafana_dashboards.schema.panel.table import Table


class TestCaseTable(TestCase):
    def setUp(self):
        super(TestCaseTable, self).setUp()
        self.schema = Table().get_schema()

    def test_defaults(self):
        defaults = {
            "columns": [],
            "editable": True,
            "error": False,
            "scroll": False,
            "showHeader": False,
            "span": 12,
            "targets": [],
            "title": "foobar",
        }

        self.assertEqual(self.schema(defaults), defaults)
