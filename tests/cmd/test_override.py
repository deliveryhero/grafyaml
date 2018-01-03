# Copyright 2018 Red Hat, Inc.
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

from testtools.matchers import MatchesRegex

from tests.cmd.base import TestCase


class TestCaseArgs(TestCase):
    path = os.path.join(
        os.path.dirname(__file__), '../fixtures/cmd/validate/test0001')

    def test_config_cli_override(self):
        required = [
            'Grafana URL override: http://example.grafana.org:3000',
            '.*?^Grafana APIKey overridden',
            '.*?^Validating schema in %s' % self.path,
        ]

        args = [
            '--grafana-url',
            'http://example.grafana.org:3000',
            '--grafana-apikey',
            'xyz',
            'validate',
            self.path,
        ]
        stdout, stderr = self.shell(' '.join(args))

        for r in required:
            self.assertThat(
                self.log_fixture.output,
                MatchesRegex(r, re.DOTALL | re.MULTILINE))

    def test_no_override(self):
        r = 'Validating schema in %s' % self.path

        args = [
            'validate',
            self.path,
        ]
        stdout, stderr = self.shell(' '.join(args))

        self.assertThat(
            self.log_fixture.output,
            MatchesRegex(r))
