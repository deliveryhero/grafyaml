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

import mock

from grafana_dashboards import builder
from tests.base import TestCase


class TestCaseBuilder(TestCase):

    def setUp(self):
        super(TestCaseBuilder, self).setUp()
        self.builder = builder.Builder(self.config)

    @mock.patch('grafana_dashboards.grafana.Dashboard.delete')
    def test_delete_dashboard(self, mock_grafana):
        path = os.path.join(
            os.path.dirname(__file__), 'fixtures/builder/dashboard-0001.yaml')

        # Create a dashboard.
        self._update_dashboard(path)
        # Create a new builder to avoid duplicate dashboards.
        builder2 = builder.Builder(self.config)
        # Delete same dashboard, ensure we delete it from grafana.
        builder2.delete_dashboard(path)
        self.assertEqual(mock_grafana.call_count, 1)

    def test_grafana_defaults(self):
        self.assertEqual(
            self.builder.grafana.server, 'http://grafana.example.org')
        self.assertEqual(self.builder.grafana.auth, None)

    @mock.patch('grafana_dashboards.grafana.Dashboard.create')
    def test_update_dashboard(self, mock_grafana):
        path = os.path.join(
            os.path.dirname(__file__), 'fixtures/builder/dashboard-0001.yaml')

        # Create a dashboard.
        self._update_dashboard(path)
        # Create a new builder to avoid duplicate dashboards.
        builder2 = builder.Builder(self.config)
        # Update again with same dashboard, ensure we don't update grafana.
        builder2.update_dashboard(path)
        self.assertEqual(mock_grafana.call_count, 0)

    @mock.patch('grafana_dashboards.grafana.Dashboard.create')
    def _update_dashboard(self, path, mock_grafana):
        self.builder.update_dashboard(path)
        # Cache is empty, so we should update grafana.
        self.assertEqual(mock_grafana.call_count, 1)
