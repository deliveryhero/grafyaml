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

import requests_mock
from testtools import TestCase

from grafana_dashboards.grafana import Grafana


class TestCaseGrafana(TestCase):

    def setUp(self):
        super(TestCaseGrafana, self).setUp()
        self.url = 'http://localhost'

    def test_init(self):
        grafana = Grafana(self.url)
        self.assertNotIn('Authorization', grafana.session.headers)

    def test_init_apikey(self):
        apikey = 'eyJrIjoiT0tTcG1pUlY2RnVKZTFVaDFsNFZXdE9ZWmNrMkZYbk'
        grafana = Grafana(self.url, apikey)
        headers = grafana.session.headers
        self.assertIn('Authorization', headers)
        self.assertEqual(headers['Authorization'], 'Bearer %s' % apikey)

    @requests_mock.Mocker()
    def test_create_dashboard_apikey(self, mock_requests):
        grafana = Grafana(self.url)
        mock_requests.register_uri('POST', '/api/dashboards/db')
        data = {
            "dashboard": {
                "title": "New dashboard",
            }
        }
        grafana.create_dashboard(data)
        self.assertEqual(mock_requests.call_count, 1)
        headers = mock_requests.last_request.headers
        self.assertIn('Content-Type', headers)
        self.assertEqual(headers['Content-Type'], 'application/json')
