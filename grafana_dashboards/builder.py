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
from oslo_log import log as logging

from grafana_dashboards.cache import Cache
from grafana_dashboards.grafana import Grafana
from grafana_dashboards.parser import YamlParser

grafana_opts = [
    cfg.StrOpt(
        'url', default='http://grafana.example.org',
        help='URL for grafana server.'),
    cfg.StrOpt(
        'apikey', default=None,
        help='API key for access grafana.'),
]

grafana_group = cfg.OptGroup(
    name='grafana', title='Grafana options')
list_opts = lambda: [(grafana_group, grafana_opts), ]

CONF = cfg.CONF
CONF.register_group(grafana_group)
CONF.register_opts(grafana_opts, group='grafana')

LOG = logging.getLogger(__name__)


class Builder(object):
    def __init__(self):
        self.cache = Cache()
        self.grafana = Grafana(CONF.grafana.url, CONF.grafana.apikey)
        self.parser = YamlParser()

    def update_dashboard(self, path):
        self.parser.parse(path)
        dashboards = self.parser.data.get('dashboard', {})
        for item in dashboards:
            data, md5 = self.parser.get_dashboard(item)
            if self.cache.has_changed(item, md5):
                self.grafana.create_dashboard(data, overwrite=True)
                self.cache.set(item, md5)
            else:
                LOG.debug("'%s' has not changed" % item)
