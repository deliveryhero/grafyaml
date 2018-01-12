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

DATASOURCE001 = {
    "id": 1,
    "orgId": 1,
    "name": "foobar",
    "type": "graphite",
    "access": "direct",
    "url": "http://example.org:8080",
    "password": "",
    "user": "",
    "database": "",
    "basicAuth": False,
    "basicAuthUser": "",
    "basicAuthPassword": "",
    "isDefault": True,
    "jsonData": None,
}

DATASOURCE_NOT_FOUND = {
    "message": "Failed to query datasources"
}


class TestCaseDatasource(TestCase):

    def setUp(self):
        super(TestCaseDatasource, self).setUp()
        self.url = 'http://localhost'
        self.grafana = Grafana(self.url)

    @requests_mock.Mocker()
    def test_create_new(self, mock_requests):
        mock_requests.post('/api/datasources/', json=DATASOURCE001)
        mock_requests.get('/api/datasources/', json=[])
        res = self.grafana.datasource.create('foobar', DATASOURCE001)
        self.assertEqual(res, DATASOURCE001)

    @requests_mock.Mocker()
    def test_get_not_found(self, mock_requests):
        mock_requests.get(
            '/api/datasources/1', json=DATASOURCE_NOT_FOUND,
            status_code=404)
        res = self.grafana.datasource.get(1)
        self.assertEqual(res, None)

    @requests_mock.Mocker()
    def test_get_success(self, mock_requests):
        mock_requests.get('/api/datasources/1', json=DATASOURCE001)
        res = self.grafana.datasource.get(1)
        self.assertEqual(res, DATASOURCE001)

    @requests_mock.Mocker()
    def test_get_all(self, mock_requests):
        mock_requests.get(
            '/api/datasources/', json=[DATASOURCE001])
        res = self.grafana.datasource.get_all()
        self.assertEqual(res, [DATASOURCE001])

    @requests_mock.Mocker()
    def test_get_all_empty(self, mock_requests):
        mock_requests.get('/api/datasources/', json=[])
        res = self.grafana.datasource.get_all()
        self.assertEqual(res, [])

    @requests_mock.Mocker()
    def test_is_datasource_empty(self, mock_requests):
        mock_requests.get('/api/datasources/', json=[])
        res = self.grafana.datasource.is_datasource('foobar')
        self.assertFalse(res)

    @requests_mock.Mocker()
    def test_is_datasource_false(self, mock_requests):
        mock_requests.get('/api/datasources/', json=[DATASOURCE001])
        res = self.grafana.datasource.is_datasource('new')
        self.assertFalse(res)

    @requests_mock.Mocker()
    def test_is_datasource_true(self, mock_requests):
        mock_requests.get('/api/datasources/', json=[DATASOURCE001])
        res = self.grafana.datasource.is_datasource('foobar')
        self.assertTrue(res)
