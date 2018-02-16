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


class Links(object):
    icons = [
        'bolt',
        'external link',
        'cloud',
        'dashboard',
        'doc',
        'info',
        'question',
    ]

    link_base = {
        v.Required('type'): v.Any('dashboards', 'link'),
        v.Optional('asDropdown'): v.All(bool),
        v.Optional('icon', default='external link'): v.Any(*icons),
        v.Optional('includeVars', default=False): v.All(bool),
        v.Optional('keepTime', default=False): v.All(bool),
        v.Optional('tags'): v.All([str]),
        v.Optional('targetBlank', default=False): v.All(bool),
        v.Optional('title'): v.All(str),
    }

    def _validate(self):

        def f(data):
            res = []
            if not isinstance(data, list):
                raise v.Invalid('Should be a list')

            for link in data:
                validate = v.Schema(self.link_base, extra=True)
                validate(link)

                if link['type'] == 'dashboards':
                    link_dashboards = {
                        v.Optional('asDropdown'): v.All(bool),
                        v.Optional('tags'): v.All([str]),
                    }
                    link_dashboards.update(self.link_base)
                    schema = v.Schema(link_dashboards)
                elif link['type'] == 'link':
                    link_link = {
                        v.Optional('tooltip'): v.All(str),
                        v.Required('url'): v.All(str),
                    }
                    link_link.update(self.link_base)
                    schema = v.Schema(link_link)

                res.append(schema(link))

            return res

        return f

    def get_schema(self):
        schema = v.Schema({
            v.Optional('links'): v.All(self._validate()),
        })

        return schema
