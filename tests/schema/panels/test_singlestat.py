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

from grafana_dashboards.schema.panel.singlestat import Singlestat


class TestCaseSinglestat(TestCase):

    def setUp(self):
        super(TestCaseSinglestat, self).setUp()
        self.schema = Singlestat().get_schema()

    def test_defaults(self):
        # Ensure default values get parsed correctly.
        defaults = {
            'colorBackground': False,
            'colorValue': False,
            'editable': True,
            'error': False,
            'maxDataPoints': 100,
            'postfix': '',
            'postfixFontSize': '50%',
            'prefix': '',
            'prefixFontSize': '50%',
            'span': 12,
            'sparkline': {
                'fillColor': 'rgba(31, 118, 189, 0.18)',
                'full': False,
                'lineColor': 'rgb(31, 120, 193)',
                'show': False
            },
            'targets': [],
            'thresholds': '',
            'title': 'foobar',
            'type': 'singlestat',
            'valueFontSize': '80%',
            'valueName': 'avg',
        }
        self.assertEqual(self.schema(defaults), defaults)
