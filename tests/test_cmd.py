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

import re

from testtools import matchers

from tests.cmd.base import TestCase


class TestCaseCmd(TestCase):

    def test_update_without_path(self):
        required = [
            '.*?^usage: grafana-dashboards update \[-h\] path',
            '.*?^grafana-dashboards update: error: (too few arguments|the '
            'following arguments are required: path)',
        ]
        stdout, stderr = self.shell('update', exitcodes=[2])
        for r in required:
            self.assertThat(
                (stdout + stderr),
                matchers.MatchesRegex(r, re.DOTALL | re.MULTILINE))

    def test_version(self):
        stdout, stderr = self.shell('--version')
        self.assertThat(
            (stdout + stderr),
            matchers.MatchesRegex('.*?^(\d+)\.(\d+)\.(\d+)'))
