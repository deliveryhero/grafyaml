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

import shutil
import tempfile

import fixtures
from oslo_config import cfg

from grafana_dashboards import config

CONF = cfg.CONF


class ConfFixture(fixtures.Fixture):
    """Fixture to manage global conf settings."""

    def setUp(self):
        super(ConfFixture, self).setUp()
        config.prepare_args([])
        self.path = tempfile.mkdtemp()
        CONF.cache.cachedir = self.path
        self.addCleanup(self._cachedir)
        self.addCleanup(CONF.reset)

    def _cachedir(self):
        shutil.rmtree(self.path)
