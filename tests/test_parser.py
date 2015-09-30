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

import os

from testtools import TestCase

from grafana_dashboards import parser


class TestCaseParser(TestCase):

    def setUp(self):
        super(TestCaseParser, self).setUp()
        self.parser = parser.YamlParser()

    def test_get_dashboard_empty(self):
        self._get_empty_dashboard('foobar')

    def test_parse_multiple(self):
        path = os.path.join(
            os.path.dirname(__file__), 'fixtures/parser/dashboard-0001.yaml')
        self.parser.parse(path)
        dashboard = {
            'foobar': {'rows': [], 'title': 'foobar'},
            'new-dashboard': {'rows': [], 'title': 'New dashboard'},
        }

        # Get parsed dashboard
        res, md5 = self.parser.get_dashboard('new-dashboard')
        self.assertEqual(res, dashboard['new-dashboard'])

        # Check for a dashboard that does not exist
        self._get_empty_dashboard('foobar')

        # Parse another file to ensure we are appending data.
        path = os.path.join(
            os.path.dirname(__file__), 'fixtures/parser/dashboard-0002.yaml')
        self.parser.parse(path)

        res, md5 = self.parser.get_dashboard('foobar')
        self.assertEqual(res, dashboard['foobar'])

        # Ensure our first dashboard still exists.
        res, md5 = self.parser.get_dashboard('new-dashboard')
        self.assertEqual(res, dashboard['new-dashboard'])

    def test_parse_duplicate(self):
        path = os.path.join(
            os.path.dirname(__file__), 'fixtures/parser/dashboard-0001.yaml')
        self.parser.parse(path)
        dashboard = {
            'new-dashboard': {'rows': [], 'title': 'New dashboard'},
        }

        # Get parsed dashboard
        res, md5 = self.parser.get_dashboard('new-dashboard')
        self.assertEqual(res, dashboard['new-dashboard'])

        path = os.path.join(
            os.path.dirname(__file__), 'fixtures/parser/dashboard-0003.yaml')
        # Fail to parse duplicate dashboard
        self.assertRaises(Exception, self.parser.parse, path)

    def _get_empty_dashboard(self, name):
        res, md5 = self.parser.get_dashboard(name)
        self.assertEqual(res, None)
