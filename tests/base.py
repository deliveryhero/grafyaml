# Copyright 2010-2011 OpenStack Foundation
# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.
# Copyright 2015 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import os
import re
import shutil
import tempfile

import fixtures
import testtools

from grafana_dashboards.config import Config

FIXTURE_DIR = os.path.join(
    os.path.dirname(__file__), 'fixtures')


def get_scenarios(fixtures_path, in_ext='yaml', out_ext='json'):
    scenarios = []
    files = []
    for dirpath, dirs, fs in os.walk(fixtures_path):
        files.extend([os.path.join(dirpath, f) for f in fs])

    input_files = [f for f in files if re.match(r'.*\.{0}$'.format(in_ext), f)]

    for input_filename in input_files:
        output_candidate = re.sub(
            r'\.{0}$'.format(in_ext), '.{0}'.format(out_ext), input_filename)
        if output_candidate not in files:
            output_candidate = None

        scenarios.append((input_filename, {
            'in_filename': input_filename,
            'out_filename': output_candidate,
        }))

    return scenarios


class TestCase(testtools.TestCase):
    """Test case base class for all unit tests."""

    def setUp(self):
        super(TestCase, self).setUp()
        self.log_fixture = self.useFixture(fixtures.FakeLogger(
            level=logging.DEBUG))
        self.setup_config()
        self.cachedir = tempfile.mkdtemp()
        self.config.set('cache', 'cachedir', self.cachedir)
        self.addCleanup(self.cleanup_cachedir)

    def setup_config(self):
        self.config = Config()
        self.config.read(os.path.join(FIXTURE_DIR, 'grafyaml.conf'))

    def cleanup_cachedir(self):
        shutil.rmtree(self.cachedir)
