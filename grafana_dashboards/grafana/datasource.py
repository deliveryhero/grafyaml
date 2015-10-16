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


class Datasource(object):

    def __init__(self, url, session):
        self.url = utils.urljoin(url, 'api/datasources/')
        self.session = session

    def create(self, name, data):
        """Create a new datasource

        :param name: URL friendly title of the datasource
        :type name: str
        :param data: Datasource model
        :type data: dict

        :raises Exception: if datasource already exists

        """
        if self.is_datasource(name):
            raise Exception('datasource[%s] already exists' % name)

        res = self.session.post(
            self.url, data=json.dumps(data))

        res.raise_for_status()
        return res.json()

    def delete(self, datasource_id):
        """Delete a datasource

        :param datasource_id: Id number of datasource
        :type datasource_id: int

        :raises Exception: if datasource failed to delete

        """
        url = utils.urljoin(self.url, str(datasource_id))
        self.session.delete(url)
        if self.get(datasource_id):
            raise Exception('datasource[%s] failed to delete' % datasource_id)

    def get(self, datasource_id):
        """Get a datasource

        :param datasource_id: Id number of datasource
        :type datasource_id: int

        :rtype: dict or None

        """
        url = utils.urljoin(self.url, str(datasource_id))
        try:
            res = self.session.get(url)
            res.raise_for_status()
        except exceptions.HTTPError:
            return None

        return res.json()

    def get_all(self):
        """List all datasource

        :rtype: dict

        """
        res = self.session.get(self.url)
        res.raise_for_status()

        return res.json()

    def is_datasource(self, name):
        """Check if a datasource exists

        :param name: URL friendly title of the dashboard
        :type name: str

        :returns: if datasource exists return id number.
        :rtype: int

        """
        datasources = self.get_all()
        for datasource in datasources:
            if datasource['name'].lower() == name.lower():
                return datasource['id']
        return 0

    def update(self, datasource_id, data):
        """Update an existing datasource

        :param datasource_id: URL friendly title of the dashboard
        :type datasource_id: int
        :param data: Datasource model
        :type data: dict
        :param overwrite: Overwrite existing dashboard with newer version or
                          with the same dashboard title
        :type overwrite: bool

        :raises Exception: if datasource already exists

        """
        url = utils.urljoin(self.url, str(datasource_id))

        res = self.session.put(
            url, data=json.dumps(data))

        res.raise_for_status()
        return res.json()
