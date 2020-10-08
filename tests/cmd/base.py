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
import sys

import fixtures
import six

from grafana_dashboards import cmd
from tests.base import TestCase


class TestCase(TestCase):
    configfile = os.path.join(os.path.dirname(__file__), "fixtures/cmd/grafyaml.conf")

    def shell(self, argstr, exitcodes=(0,)):
        orig = sys.stdout
        orig_stderr = sys.stderr
        try:
            sys.stdout = six.StringIO()
            sys.stderr = six.StringIO()
            argv = [
                "grafana-dashboards",
                "--config-file=%s" % self.configfile,
            ]
            argv += argstr.split()
            self.useFixture(fixtures.MonkeyPatch("sys.argv", argv))
            cmd.main()
        except SystemExit:
            exc_type, exc_value, exc_trackback = sys.exc_info()
            self.assertIn(exc_value.code, exitcodes)
        finally:
            stdout = sys.stdout.getvalue()
            sys.stdout.close()
            sys.stdout = orig
            stderr = sys.stderr.getvalue()
            sys.stderr.close()
            sys.stderr = orig_stderr
        return (stdout, stderr)
