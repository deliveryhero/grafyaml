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

from grafana_dashboards.schema.panel import Panel


class Row(object):

    def get_schema(self):
        row = {
            v.Required('collapse', default=False): v.All(bool),
            v.Required('editable', default=True): v.All(bool),
            v.Required('height'): v.All(str),
            v.Required('showTitle', default=False): v.All(bool),
            v.Required('title'): v.All(str, v.Length(min=1)),
        }
        panels = Panel().get_schema()
        row.update(panels.schema)
        schema = v.Schema({
            v.Required('rows', default=[]): [row],
        })

        return schema
