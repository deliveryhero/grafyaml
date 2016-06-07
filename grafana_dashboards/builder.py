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
        self.cache = Cache(
            config.get('cache', 'cachedir'),
            config.getboolean('cache', 'enabled'))
        self.grafana = Grafana(
            url=config.get('grafana', 'url'),
            key=config.get('grafana', 'apikey'))
        self.parser = YamlParser()

    def delete(self, path):
        self.load_files(path)
        datasources = self.parser.data.get('datasource', {})
        LOG.info('Number of datasources to be deleted: %d', len(datasources))
        self._delete_datasource(datasources)
        dashboards = self.parser.data.get('dashboard', {})
        LOG.info('Number of dashboards to be deleted: %d', len(dashboards))
        self._delete_dashboard(dashboards)

    def load_files(self, path):
        files_to_process = []
        paths = path.split(':')
        for path in paths:
            if os.path.isdir(path):
                files_to_process.extend([os.path.join(path, f)
                                         for f in os.listdir(path)
                                         if (f.endswith('.yaml')
                                             or f.endswith('.yml'))])
            else:
                files_to_process.append(path)

        for fn in files_to_process:
            self.parser.parse(fn)

    def update(self, path):
        self.load_files(path)
        datasources = self.parser.data.get('datasource', {})
        LOG.info('Number of datasources to be updated: %d', len(datasources))
        self._update_datasource(datasources)
        dashboards = self.parser.data.get('dashboard', {})
        LOG.info('Number of dashboards to be updated: %d', len(dashboards))
        self._update_dashboard(dashboards)

    def _delete_dashboard(self, data):
        for name in data:
            LOG.debug('Deleting grafana dashboard %s', name)
            self.grafana.dashboard.delete(name)
            self.cache.set(name, '')

    def _delete_datasource(self, data):
        for name in data:
            LOG.debug('Deleting grafana datasource %s', name)
            datasource_id = self.grafana.datasource.is_datasource(name)
            if datasource_id:
                self.grafana.datasource.delete(datasource_id)
                self.cache.set(name, '')

    def _update_dashboard(self, data):
        for name in data:
            data, md5 = self.parser.get_dashboard(name)
            if self.cache.has_changed(name, md5):
                self.grafana.dashboard.create(name, data, overwrite=True)
                self.cache.set(name, md5)
            else:
                LOG.debug("'%s' has not changed" % name)

    def _update_datasource(self, data):
        for name in data:
            data, md5 = self.parser.get_datasource(name)
            if self.cache.has_changed(name, md5):
                # Check for existing datasource so we can find the
                # datasource_id.
                datasource_id = self.grafana.datasource.is_datasource(name)
                if datasource_id:
                    self.grafana.datasource.update(datasource_id, data)
                else:
                    self.grafana.datasource.create(name, data)
                self.cache.set(name, md5)
            else:
                LOG.debug("'%s' has not changed" % name)
