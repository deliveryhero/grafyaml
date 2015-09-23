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

from requests_mock.contrib import fixture as rm_fixture
from testtools import TestCase

from grafana_dashboards import grafana


class TestCaseGrafana(TestCase):

    def setUp(self):
        super(TestCaseGrafana, self).setUp()
        self.apikey = 'eyJrIjoiT0tTcG1pUlY2RnVKZTFVaDFsNFZXdE9ZWmNrMkZYbk'
        self.url = 'http://localhost'
        self.grafana = grafana.Grafana(self.url, self.apikey)

    def test_create_dashboard(self):
        mock_requests = self.useFixture(rm_fixture.Fixture())
        mock_requests.post('/api/dashboards/db')
        data = {
            "dashboard": {
                "title": "New dashboard",
            }
        }
        self.grafana.create_dashboard(data)
        self.assertEqual(mock_requests.call_count, 1)
        headers = mock_requests.last_request.headers
        self._test_headers(headers)

    def _test_headers(self, headers):
        self.assertIn('Authorization', headers)
        self.assertEqual(headers['Authorization'], 'Bearer %s' % self.apikey)
        self.assertIn('Content-Type', headers)
        self.assertEqual(headers['Content-Type'], 'application/json')
