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
        self.builder = builder.Builder()

    @mock.patch('grafana_dashboards.grafana.Grafana.create_dashboard')
    def test_update_dashboard(self, mock_grafana):
        dashboard = os.path.join(
            os.path.dirname(__file__), 'fixtures/builder/dashboard-0001.yaml')

        self.builder.update_dashboard(dashboard)
        # Cache is empty, so we should update grafana.
        self.assertEqual(mock_grafana.call_count, 1)

        # Create a new builder to avoid duplicate dashboards.
        builder2 = builder.Builder()
        # Update again with same dashboard, ensure we don't update grafana.
        builder2.update_dashboard(dashboard)
        self.assertEqual(mock_grafana.call_count, 1)
