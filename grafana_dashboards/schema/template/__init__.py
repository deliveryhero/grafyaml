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

from grafana_dashboards.schema.template.base import Base
from grafana_dashboards.schema.template.interval import Interval
from grafana_dashboards.schema.template.query import Query


class Template(object):

    def __init__(self):
        # TODO(pabelanger): This is pretty ugly, there much be a better way to
        # set default values.
        self.defaults = {
            'enabled': False,
            'list': [],
        }

    def _validate(self):

        def f(data):
            res = self.defaults
            if not isinstance(data, list):
                raise v.Invalid('Should be a list')

            for template in data:
                res['enabled'] = True
                validate = Base().get_schema()
                validate(template)

                if template['type'] == 'query':
                    schema = Query().get_schema()
                if template['type'] == 'interval':
                    schema = Interval().get_schema()

                res['list'].append(schema(template))

            return res

        return f

    def get_schema(self):
        schema = v.Schema({
            v.Required(
                'templating', default=self.defaults): v.All(
                    self._validate()),
        })

        return schema
