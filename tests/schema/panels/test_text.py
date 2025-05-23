# Copyright 2015 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from testtools import TestCase

from grafana_dashboards.schema.panel.text import Text


class TestCaseText(TestCase):
    def setUp(self):
        super(TestCaseText, self).setUp()
        self.schema = Text().get_schema()

    def test_minimum(self):
        # Ensure minimum values get parsed correctly and default mode gets set
        defaults = {
            "type": "text",
            "title": "Panel Title",
            "gridPos": {
                "h": 8,
                "w": 8,
                "x": 0,
                "y": 0,
            },
            "options": {
                "content": "# Title\n\nFor markdown syntax help: [commonmark.org/help](https://commonmark.org/help/)",
            },
        }
        observed = self.schema(defaults)
        expected = defaults
        expected["options"]["mode"] = "markdown"
        self.assertEqual(expected, observed)

    def test_defaults(self):
        # Ensure default values get parsed correctly.
        defaults = {
            "type": "text",
            "title": "Panel Title",
            "gridPos": {
                "h": 8,
                "w": 8,
                "x": 0,
                "y": 0,
            },
            "options": {
                "mode": "markdown",
                "code": {
                    "language": "plaintext",
                    "showLineNumbers": False,
                    "showMiniMap": False,
                },
                "content": "# Title\n\nFor markdown syntax help: [commonmark.org/help](https://commonmark.org/help/)",
            },
        }
        self.assertEqual(self.schema(defaults), defaults)
