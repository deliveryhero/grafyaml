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

from oslo_config import cfg

from grafana_dashboards.grafana import Grafana
from grafana_dashboards.parser import YamlParser
from grafana_dashboards.schema.dashboard import Dashboard

grafana_opts = [
    cfg.StrOpt(
        'url', default='http://grafana.example.org',
        help='URL for grafana server.'),
    cfg.StrOpt(
        'apikey', default='',
        help='API key for access grafana.'),
]

grafana_group = cfg.OptGroup(
    name='grafana', title='Grafana options')
list_opts = lambda: [(grafana_group, grafana_opts), ]

CONF = cfg.CONF
CONF.register_group(grafana_group)
CONF.register_opts(grafana_opts, group='grafana')


class Builder(object):
    def __init__(self):
        self.grafana = Grafana(CONF.grafana.url, CONF.grafana.apikey)
        self.parser = YamlParser()

    def update_dashboard(self, path):
        data = self.parser.load(path)
        schema = Dashboard()
        result = schema.validate(data)
        self.grafana.create_dashboard(result, overwrite=True)
