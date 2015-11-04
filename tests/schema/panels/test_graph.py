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

from grafana_dashboards.schema.panel.graph import Graph


class TestCaseGraph(TestCase):

    def setUp(self):
        super(TestCaseGraph, self).setUp()
        self.schema = Graph().get_schema()

    def test_defaults(self):
        # Ensure default values get parsed correctly.
        defaults = {
            'bars': False,
            'editable': True,
            'error': False,
            'fill': 1,
            'lines': True,
            'linewidth': 2,
            'percentage': False,
            'pointradius': 5,
            'points': False,
            'span': 12,
            'stack': False,
            'steppedLine': False,
            'targets': [],
            'title': 'foobar',
            'type': 'graph',
            'x-axis': True,
            'y-axis': True,
        }
        self.assertEqual(self.schema(defaults), defaults)
