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

import voluptuous as v

from grafana_dashboards.schema.panel.base import Base
from grafana_dashboards.schema.panel.dashlist import Dashlist
from grafana_dashboards.schema.panel.graph import Graph
from grafana_dashboards.schema.panel.singlestat import Singlestat
from grafana_dashboards.schema.panel.text import Text


class Panel(object):

    def _validate(self):

        def f(data):
            res = []
            if not isinstance(data, list):
                raise v.Invalid('Should be a list')

            for panel in data:
                validate = Base().get_schema()
                validate(panel)

                if panel['type'] == 'dashlist':
                    schema = Dashlist().get_schema()
                elif panel['type'] == 'graph':
                    schema = Graph().get_schema()
                elif panel['type'] == 'singlestat':
                    schema = Singlestat().get_schema()
                elif panel['type'] == 'text':
                    schema = Text().get_schema()

                res.append(schema(panel))

            return res

        return f

    def get_schema(self):
        schema = v.Schema({
            v.Required('panels', default=[]): v.All(self._validate()),
        })

        return schema
