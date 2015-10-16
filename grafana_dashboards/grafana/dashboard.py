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

import json

from requests import exceptions

from grafana_dashboards.grafana import utils


class Dashboard(object):

    def __init__(self, url, session):
        self.url = utils.urljoin(url, 'api/dashboards/db/')
        self.session = session

    def create(self, name, data, overwrite=False):
        """Create a new dashboard

        :param name: URL friendly title of the dashboard
        :type name: str
        :param data: Dashboard model
        :type data: dict
        :param overwrite: Overwrite existing dashboard with newer version or
                          with the same dashboard title
        :type overwrite: bool

        :raises Exception: if dashboard already exists

        """
        dashboard = {
            'dashboard': data,
            'overwrite': overwrite,
        }
        if not overwrite and self.is_dashboard(name):
            raise Exception('dashboard[%s] already exists' % name)

        res = self.session.post(
            self.url, data=json.dumps(dashboard))
        res.raise_for_status()
        if not self.is_dashboard(name):
            raise Exception('dashboard[%s] does not exist' % name)

    def delete(self, name):
        """Delete a dashboard

        :param name: URL friendly title of the dashboard
        :type name: str

        :raises Exception: if dashboard failed to delete

        """
        url = utils.urljoin(self.url, name)
        self.session.delete(url)
        if self.is_dashboard(name):
            raise Exception('dashboard[%s] failed to delete' % name)

    def get(self, name):
        """Get a dashboard

        :param name: URL friendly title of the dashboard
        :type name: str

        :rtype: dict or None

        """
        url = utils.urljoin(self.url, name)
        try:
            res = self.session.get(url)
            res.raise_for_status()
        except exceptions.HTTPError:
            return None

        return res.json()

    def is_dashboard(self, name):
        """Check if a dashboard exists

        :param name: URL friendly title of the dashboard
        :type name: str

        :returns: True if dashboard exists
        :rtype: bool

        """
        res = self.get(name)
        if res and res['meta']['slug'] == name:
            return True
        return False
