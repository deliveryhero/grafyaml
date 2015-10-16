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

import requests

from grafana_dashboards.grafana.dashboard import Dashboard
from grafana_dashboards.grafana.datasource import Datasource


class Grafana(object):

    def __init__(self, url, key=None):
        """Create object for grafana instance

        :param url: URL for Grafana server
        :type url: str
        :param key: API token used for authenticate
        :type key: str

        """
        self.server = url
        self.auth = None

        session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/json',
        })
        # NOTE(pabelanger): Grafana 2.1.0 added basic auth support so now the
        # api key is optional.
        if key:
            self.auth = {'Authorization': 'Bearer %s' % key}
            session.headers.update(self.auth)

        self.dashboard = Dashboard(self.server, session)
        self.datasource = Datasource(self.server, session)
