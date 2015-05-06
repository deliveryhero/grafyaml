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
import re
import yaml

from testtools import TestCase

from grafana_dashboards.schema import dashboard

FIXTURE_DIR = os.path.join(os.path.dirname(__file__),
                           'fixtures')
LAYOUT_RE = re.compile(r'^(dashboard)-.*\.yaml$')


class TestCaseSchemaDashboard(TestCase):
    def test_layouts(self):
        for fn in os.listdir(os.path.join(FIXTURE_DIR)):
            schema = None
            m = LAYOUT_RE.match(fn)
            if not m:
                continue
            layout = os.path.join(FIXTURE_DIR, fn)
            data = yaml.load(open(layout))

            if m.group(1) == 'dashboard':
                schema = dashboard.Dashboard()

            schema.validate(data)
