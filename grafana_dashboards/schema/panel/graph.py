# -*- coding: utf-8 -*-

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


class Graph(Base):

    def get_schema(self):
        y_format = v.Any(
            u'none',
            u'short',
            u'percent',
            u'percentunit',
            u'humidity',
            u'ppm',
            u'dB',
            u'currencyUSD',
            u'currencyGBP',
            u'currencyEUR',
            u'currencyJPY',
            u'hertz',
            u'ns',
            u'µs',
            u'ms',
            u's',
            u'm',
            u'h',
            u'd',
            u'bits',
            u'bytes',
            u'kbytes',
            u'mbytes',
            u'gbytes',
            u'pps',
            u'bps',
            u'Bps',
            u'ops',
            u'rps',
            u'wps',
            u'iops',
            u'lengthmm',
            u'lengthm',
            u'lengthkm',
            u'lengthmi',
            u'velocityms',
            u'velocitykmh',
            u'velocitymph',
            u'velocityknot',
            u'mlitre',
            u'litre',
            u'm3',
            u'watt',
            u'kwatt',
            u'watth',
            u'kwatth',
            u'joule',
            u'ev',
            u'amp',
            u'volt',
            u'celsius',
            u'farenheit',
            u'kelvin',
            u'pressurembar',
            u'pressurehpa',
            u'pressurehg',
            u'pressurepsi',
        )

        y_formats = [y_format]

        graph = {
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
            v.Optional('leftYAxisLabel'): v.All(str, v.Length(min=1)),
            v.Optional('rightYAxisLabel'): v.All(str, v.Length(min=1)),
            v.Optional('y_formats'): v.All(y_formats, v.Length(min=2, max=2)),
        }
        graph.update(self.base)
        return v.Schema(graph)
