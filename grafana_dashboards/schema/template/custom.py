# Copyright 2018 Red Hat, Inc.
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


class Custom(Base):
    current = {
        v.Required('text'): v.All(str, v.Length(min=1)),
        v.Required('value'): v.All([str]),
    }

    def validate_options(self, options):
        options = self._validate_options(options)

        if len(options):
            selected_options = [x for x in options if x.get('selected')]
            # Default to first option as selected (if nothing selected)
            if len(selected_options) == 0:
                options[0]['selected'] = True

        return options

    def _validate(self, data):
        custom = {
            v.Required('current'): v.Any(self.current),
            v.Required('includeAll', default=False): v.All(bool),
            v.Required('multi', default=False): v.All(bool),
            v.Required('options', default=[]): self.validate_options,
            v.Required('query', default=''): v.All(str),
            v.Optional('allValue'): v.All(str),
            v.Optional('hide'): v.All(int, v.Range(min=0, max=2)),
            v.Optional('label', default=''): v.All(str),

        }
        custom.update(self.base)

        custom_options_schema = {
            v.Required('options', default=[]): self.validate_options,
        }
        data = v.Schema(custom_options_schema, extra=True)(data)

        # If 'query' is not supplied, compose it from the list of options.
        if 'query' not in data:
            query = [option['text']
                     for option in data.get('options')
                     if option['text'] != 'All']
            data['query'] = ','.join(query)

        if 'current' not in data:
            selected = [option['text']
                        for option in data.get('options')
                        if option['selected']]
            data['current'] = dict(text='+'.join(selected), value=selected)

        return v.Schema(custom)(data)

    def get_schema(self):
        return v.Schema(self._validate)
