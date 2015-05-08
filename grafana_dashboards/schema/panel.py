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


class Panel(object):

    def __init__(self):
        self.base = {
            v.Required('editable', default=True): v.All(bool),
            v.Required('error', default=False): v.All(bool),
            v.Required('span', default=12): v.All(int, v.Range(min=0, max=12)),
            v.Required('title'): v.All(str, v.Length(min=1)),
            v.Required('type'): v.Any('dashlist', 'text'),
            v.Optional('id'): int,
        }

        self.dashlist = {
            v.Required('limit', default=10): v.All(int),
            v.Required('mode', default='starred'): v.Any('search', 'starred'),
            v.Required('tag', default=''): v.All(str),
            v.Required('query', default=''): v.All(str),
        }
        self.dashlist.update(self.base)

        self.text = {
            v.Required('content'): v.All(str),
            v.Required('mode', default='markdown'): v.Any(
                'html', 'markdown', 'text'),
            v.Optional('style'): dict(),
        }
        self.text.update(self.base)

    def _validate(self):
        res = []

        def f(data):
            if not isinstance(data, list):
                raise v.Invalid('Should be a list')

            for x in data:
                schema = v.Schema(self.base, extra=True)
                schema(x)
                if x['type'] == 'text':
                    panel = v.Schema(self.text)
                elif x['type'] == 'dashlist':
                    panel = v.Schema(self.dashlist)

                res.append(panel(x))

            return res

        return f

    def get_schema(self):
        schema = v.Schema({
            v.Required('panels', default=[]): v.All(self._validate()),
        })

        return schema
