# -*- coding: utf-8 -*-

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

import doctest
import json
import os
import re
import testtools

from grafana_dashboards.parser import YamlParser
from grafana_dashboards.schema import dashboard


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


class TestCase(object):
    """Test case base class for all unit tests."""
    parser = YamlParser()

    def _read_raw_content(self):
        # if None assume empty file
        if self.out_filename is None:
            return ""

        content = open(self.out_filename, 'r').read()

        return content

    def test_yaml_snippet(self):
        expected_json = self._read_raw_content()
        yaml_content = self.parser.load(self.in_filename)

        schema = dashboard.Dashboard()
        valid_yaml = schema.validate(yaml_content)
        pretty_json = json.dumps(
            valid_yaml, indent=4, separators=(',', ': '), sort_keys=True)

        self.assertThat(pretty_json, testtools.matchers.DocTestMatches(
            expected_json, doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE |
            doctest.REPORT_NDIFF))
