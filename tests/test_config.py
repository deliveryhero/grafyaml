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

from grafana_dashboards.config import Config
from tests.base import TestCase


class TestCaseConfig(TestCase):

    def setUp(self):
        super(TestCaseConfig, self).setUp()
        self.config = Config()

    def test_defaults(self):
        self.assertTrue(
            self.config.getboolean('cache', 'enabled'))
        self.assertEqual(
            self.config.get('cache', 'cachedir'), '~/.cache/grafyaml')
        self.assertEqual(
            self.config.get('grafana', 'apikey'), '')
        self.assertEqual(
            self.config.get('grafana', 'url'), 'http://localhost:8080')
