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

from grafana_dashboards.schema.panel.dashlist import Dashlist


class TestCaseDashlist(TestCase):

    def setUp(self):
        super(TestCaseDashlist, self).setUp()
        self.schema = Dashlist().get_schema()

    def test_defaults(self):
        # Ensure default values get parsed correctly.
        defaults = {
            'editable': True,
            'error': False,
            'limit': 10,
            'mode': 'starred',
            'query': '',
            'span': 12,
            'tag': '',
            'title': 'foobar',
            'type': 'dashlist',
        }
        self.assertEqual(self.schema(defaults), defaults)
