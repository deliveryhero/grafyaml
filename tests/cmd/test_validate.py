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

from testscenarios.testcase import TestWithScenarios
from testtools import matchers

from tests.base import get_scenarios
from tests.cmd.base import TestCase


class TestCaseValidateScenarios(TestWithScenarios, TestCase):
    fixtures_path = os.path.join(
        os.path.dirname(__file__), '../fixtures/cmd/validate')
    scenarios = get_scenarios(fixtures_path)

    def test_command(self):
        if os.path.basename(self.in_filename).startswith('good-'):
            self._validate_success()
        else:
            self._validate_failure()

    def _validate_failure(self):
        required = [
            '%s: ERROR:' % self.in_filename,
        ]
        stdout, stderr = self.shell(
            'validate %s' % self.in_filename, exitcodes=[1])
        for r in required:
            self.assertThat(
                (stdout + stderr),
                matchers.MatchesRegex(r, re.DOTALL | re.MULTILINE))

    def _validate_success(self):
        required = [
            'SUCCESS!',
        ]
        stdout, stderr = self.shell(
            'validate %s' % self.in_filename, exitcodes=[0])
        for r in required:
            self.assertThat(
                (stdout + stderr),
                matchers.MatchesRegex(r, re.DOTALL | re.MULTILINE))


class TestCaseValidate(TestCase):

    def test_validate_directory_success(self):
        path = os.path.join(
            os.path.dirname(__file__), '../fixtures/cmd/validate/test0001')
        required = [
            'SUCCESS!',
        ]
        stdout, stderr = self.shell(
            'validate %s' % path, exitcodes=[0])
        for r in required:
            self.assertThat(
                (stdout + stderr),
                matchers.MatchesRegex(r, re.DOTALL | re.MULTILINE))

    def test_validate_directory_invalid(self):
        path = os.path.join(
            os.path.dirname(__file__), '../fixtures/cmd/validate/__invalid__')
        self._validate_invalid_file_or_directory(path)

    def test_validate_file_invalid(self):
        path = os.path.join(
            os.path.dirname(__file__), '../fixtures/cmd/validate/invalid.yaml')
        self._validate_invalid_file_or_directory(path)

    def _validate_invalid_file_or_directory(self, path):
        required = [
            '%s: ERROR: \[Errno 2\] No such file or directory:' % path,
        ]
        stdout, stderr = self.shell(
            'validate %s' % path, exitcodes=[1])
        for r in required:
            self.assertThat(
                (stdout + stderr),
                matchers.MatchesRegex(r, re.DOTALL | re.MULTILINE))

    def test_validate_without_path(self):
        required = [
            '.*?^usage: grafana-dashboards validate \[-h\] path',
            '.*?^grafana-dashboards validate: error: (too few arguments|the '
            'following arguments are required: path)',
        ]
        stdout, stderr = self.shell('validate', exitcodes=[2])
        for r in required:
            self.assertThat(
                (stdout + stderr),
                matchers.MatchesRegex(r, re.DOTALL | re.MULTILINE))
