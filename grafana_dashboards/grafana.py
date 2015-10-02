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

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

import requests
from requests import exceptions


class Grafana(object):

    def __init__(self, url, key=None):
        """Create object for grafana instance

        :param url: URL for Grafana server
        :type url: str
        :param key: API token used for authenticate
        :type key: str

        """

        self.url = urljoin(url, 'api/dashboards/db/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
        })
        # NOTE(pabelanger): Grafana 2.1.0 added basic auth support so now the
        # api key is optional.
        if key:
            self.session.headers.update({
                'Authorization': 'Bearer %s' % key,
            })

    def assert_dashboard_exists(self, name):
        """Raise an exception if dashboard does not exist

        :param name: URL friendly title of the dashboard
        :type name: str
        :raises Exception: if dashboard does not exist

        """
        if not self.is_dashboard(name):
            raise Exception('dashboard[%s] does not exist' % name)

    def create_dashboard(self, name, data, overwrite=False):
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
        self.assert_dashboard_exists(name)

    def get_dashboard(self, name):
        """Get a dashboard

        :param name: URL friendly title of the dashboard
        :type name: str

        :rtype: dict or None

        """
        url = urljoin(self.url, name)
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
        res = self.get_dashboard(name)
        if res and res['meta']['slug'] == name:
            return True
        return False
