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

CREATE_NEW_DASHBOARD = {
    "meta": {
        "canSave": True,
        "created": "0001-01-01T00:00:00Z",
        "canStar": True,
        "expires": "0001-01-01T00:00:00Z",
        "slug": "new-dashboard",
        "type": "db",
        "canEdit": True
    },
    "dashboard": {
        "rows": [],
        "id": 1,
        "version": 0,
        "title": "New dashboard"
    }
}

DASHBOARD_NOT_FOUND = {
    "message": "Dashboard not found"
}


class TestCaseGrafana(TestCase):

    def setUp(self):
        super(TestCaseGrafana, self).setUp()
        self.url = 'http://localhost'
        self.grafana = Grafana(self.url)

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
    def test_assert_dashboard_exists_failure(self, mock_requests):
        mock_requests.get(
            '/api/dashboards/db/new-dashboard', json=DASHBOARD_NOT_FOUND,
            status_code=404)
        self.assertRaises(
            Exception, self.grafana.assert_dashboard_exists, 'new-dashboard')

    @requests_mock.Mocker()
    def test_create_dashboard_new(self, mock_requests):
        def post_callback(request, context):
            mock_requests.get(
                '/api/dashboards/db/new-dashboard', json=CREATE_NEW_DASHBOARD)
            return True

        mock_requests.post('/api/dashboards/db/', json=post_callback)
        mock_requests.get(
            '/api/dashboards/db/new-dashboard', json=DASHBOARD_NOT_FOUND,
            status_code=404)

        data = {
            "dashboard": {
                "title": "New dashboard",
            },
            "slug": 'new-dashboard',
        }
        self.grafana.create_dashboard(
            name=data['slug'], data=data['dashboard'])
        self.assertEqual(mock_requests.call_count, 3)

    @requests_mock.Mocker()
    def test_create_dashboard_overwrite(self, mock_requests):
        mock_requests.post('/api/dashboards/db/')
        mock_requests.get(
            '/api/dashboards/db/new-dashboard', json=CREATE_NEW_DASHBOARD)
        data = {
            "dashboard": {
                "title": "New dashboard",
            },
            "slug": 'new-dashboard',
        }
        self.grafana.create_dashboard(
            name=data['slug'], data=data['dashboard'], overwrite=True)
        self.assertEqual(mock_requests.call_count, 2)

    @requests_mock.Mocker()
    def test_create_dashboard_existing(self, mock_requests):
        mock_requests.post('/api/dashboards/db/')
        mock_requests.get(
            '/api/dashboards/db/new-dashboard', json=CREATE_NEW_DASHBOARD)
        data = {
            "dashboard": {
                "title": "New dashboard",
            },
            "slug": 'new-dashboard',
        }
        self.assertRaises(
            Exception, self.grafana.create_dashboard, name=data['slug'],
            data=data['dashboard'], overwrite=False)

        self.assertEqual(mock_requests.call_count, 1)
