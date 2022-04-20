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

import json

import testtools
import testtools.matchers

from grafana_dashboards.parser import YamlParser


class TestCase(object):
    """Test case base class for all unit tests."""

    def _read_raw_content(self):
        # if None assume empty file
        if self.out_filename is None:
            return ""

        content = open(self.out_filename, "r").read()

        return content

    def test_yaml_snippet(self):
        parser = YamlParser()
        expected_json = json.loads(self._read_raw_content(), strict=True)
        parser.parse(self.in_filename)
        valid_yaml = parser.data

        self.assertThat(valid_yaml, testtools.matchers.Equals(expected_json))
