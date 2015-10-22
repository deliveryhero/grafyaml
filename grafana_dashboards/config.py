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

from six.moves import configparser as ConfigParser


class Config(ConfigParser.ConfigParser):

    def __init__(self):
        ConfigParser.ConfigParser.__init__(self)
        # Add [cache] section
        self.add_section('cache')
        self.set('cache', 'cachedir', '~/.cache/grafyaml')
        self.set('cache', 'enabled', 'true')
        # Add [grafana] section
        self.add_section('grafana')
        self.set('grafana', 'apikey', '')
        self.set('grafana', 'url', 'http://localhost:8080')
