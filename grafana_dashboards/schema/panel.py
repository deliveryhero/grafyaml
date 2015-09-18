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
            v.Required('type'): v.Any(
                'dashlist', 'graph', 'singlestat', 'text'),
            v.Optional('id'): int,
        }

        self.dashlist = {
            v.Required('limit', default=10): v.All(int),
            v.Required('mode', default='starred'): v.Any('search', 'starred'),
            v.Required('tag', default=''): v.All(str),
            v.Required('query', default=''): v.All(str),
        }
        self.dashlist.update(self.base)

        self.graph = {
            v.Required('bars', default=False): v.All(bool),
            v.Required('fill', default=1): v.All(int),
            v.Required('lines', default=True): v.All(bool),
            v.Required('linewidth', default=2): v.All(int),
            v.Required('percentage', default=False): v.All(bool),
            v.Required('pointradius', default=5): v.All(int),
            v.Required('points', default=False): v.All(bool),
            v.Required('stack', default=False): v.All(bool),
            v.Required('steppedLine', default=False): v.All(bool),
            v.Required('targets', default=[]): v.All(list),
            v.Required('x-axis', default=True): v.All(bool),
            v.Required('y-axis', default=True): v.All(bool),
        }
        self.graph.update(self.base)

        # TODO(pabelanger): This is pretty ugly, there much be a better way to
        # set default values.
        sparkline_defaults = {
            'fillColor': 'rgba(31, 118, 189, 0.18)',
            'full': False,
            'lineColor': 'rgb(31, 120, 193)',
            'show': False,
        }
        sparkline = {
            v.Required(
                'fillColor', default=sparkline_defaults['fillColor']
            ): v.All(str),
            v.Required('full', default=False): v.All(bool),
            v.Required(
                'lineColor', default=sparkline_defaults['lineColor']
            ): v.All(str),
            v.Required('show', default=False): v.All(bool),
        }

        self.singlestat = {
            v.Required('colorBackground', default=False): v.All(bool),
            v.Required('colorValue', default=False): v.All(bool),
            v.Required('maxDataPoints', default=100): v.All(int),
            v.Required('sparkline', default=sparkline_defaults): sparkline,
            v.Required('targets', default=[]): v.All(list),
            v.Required('thresholds', default=''): v.All(str),
            v.Required('valueName', default='avg'): v.All(
                'avg', 'current', 'max', 'min', 'total'),
        }
        self.singlestat.update(self.base)

        self.text = {
            v.Required('content'): v.All(str),
            v.Required('mode', default='markdown'): v.Any(
                'html', 'markdown', 'text'),
            v.Optional('style'): dict(),
        }
        self.text.update(self.base)

    def _validate(self):

        def f(data):
            res = []
            if not isinstance(data, list):
                raise v.Invalid('Should be a list')

            for panel in data:
                validate = v.Schema(self.base, extra=True)
                validate(panel)

                if panel['type'] == 'dashlist':
                    schema = v.Schema(self.dashlist)
                elif panel['type'] == 'graph':
                    schema = v.Schema(self.graph)
                elif panel['type'] == 'singlestat':
                    schema = v.Schema(self.singlestat)
                elif panel['type'] == 'text':
                    schema = v.Schema(self.text)

                res.append(schema(panel))

            return res

        return f

    def get_schema(self):
        schema = v.Schema({
            v.Required('panels', default=[]): v.All(self._validate()),
        })

        return schema
