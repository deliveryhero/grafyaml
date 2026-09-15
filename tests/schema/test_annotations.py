import voluptuous as v
from testtools import TestCase

from grafana_dashboards.schema.annotations import Annotations


class TestCaseAnnotations(TestCase):
    def setUp(self):
        super(TestCaseAnnotations, self).setUp()
        self.schema = Annotations().get_schema()
        self.base = {
            "annotations": {
                "list": [
                    {
                        "name": "test",
                        "datasource": "grafanacloud-prom",
                        "enable": True,
                        "hide": False,
                        "expr": "sum(up)",
                    }
                ]
            }
        }

    def test_datasource_string(self):
        self.schema(self.base)

    def test_datasource_dict(self):
        annotation = self.base["annotations"]["list"][0]
        annotation["datasource"] = {"type": "loki", "uid": "grafanacloud-logs"}
        self.schema(self.base)

    def test_datasource_dict_uid_only(self):
        annotation = self.base["annotations"]["list"][0]
        annotation["datasource"] = {"uid": "grafanacloud-logs"}
        self.schema(self.base)

    def test_datasource_invalid(self):
        annotation = self.base["annotations"]["list"][0]
        annotation["datasource"] = 42
        self.assertRaises(v.Invalid, self.schema, self.base)

    def test_missing_datasource(self):
        annotation = self.base["annotations"]["list"][0]
        del annotation["datasource"]
        self.assertRaises(v.Invalid, self.schema, self.base)
