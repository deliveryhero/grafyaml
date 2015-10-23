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

import logging
import os

from grafana_dashboards.cache import Cache
from grafana_dashboards.grafana import Grafana
from grafana_dashboards.parser import YamlParser

LOG = logging.getLogger(__name__)


class Builder(object):

    def __init__(self, config):
        self.grafana = Grafana(
            config.get('grafana', 'apikey'), config.get('grafana', 'url'))
        self.parser = YamlParser()
        self.cache_enabled = config.getboolean('cache', 'enabled')
        self.cache = Cache(config.get('cache', 'cachedir'))

    def delete_dashboard(self, path):
        self.load_files(path)
        dashboards = self.parser.data.get('dashboard', {})
        for name in dashboards:
            LOG.debug('Deleting grafana dashboard %s', name)
            self.grafana.dashboard.delete(name)
            self.cache.set(name, '')

    def load_files(self, path):
        files_to_process = []
        if os.path.isdir(path):
            files_to_process.extend([os.path.join(path, f)
                                     for f in os.listdir(path)
                                     if (f.endswith('.yaml')
                                         or f.endswith('.yml'))])
        else:
            files_to_process.append(path)

        for fn in files_to_process:
            self.parser.parse(fn)

    def update_dashboard(self, path):
        self.load_files(path)
        dashboards = self.parser.data.get('dashboard', {})
        LOG.info('Number of dashboards generated: %d', len(dashboards))
        for name in dashboards:
            data, md5 = self.parser.get_dashboard(name)
            if self.cache.has_changed(name, md5) or not self.cache_enabled:
                self.grafana.dashboard.create(name, data, overwrite=True)
                self.cache.set(name, md5)
            else:
                LOG.debug("'%s' has not changed" % name)
