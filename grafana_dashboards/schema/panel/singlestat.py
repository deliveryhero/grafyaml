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


class Singlestat(Base):

    def get_schema(self):
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

        singlestat = {
            v.Required('colorBackground', default=False): v.All(bool),
            v.Required('colorValue', default=False): v.All(bool),
            v.Required('maxDataPoints', default=100): v.All(int),
            v.Required('postfix', default=''): v.All(str),
            # Support 0% to 200% by 10
            v.Required(
                'postfixFontSize', default='50%'): v.All(
                    v.Match(r'^[1-9]?[0]{1}%$|^1[0-9]?[0]{1}%$|^200%$')),
            v.Required('prefix', default=''): v.All(str),
            # Support 0% to 200% by 10
            v.Required(
                'prefixFontSize', default='50%'): v.All(
                    v.Match(r'^[1-9]?[0]{1}%$|^1[0-9]?[0]{1}%$|^200%$')),
            v.Required('sparkline', default=sparkline_defaults): sparkline,
            v.Required('targets', default=[]): v.All(list),
            v.Required('thresholds', default=''): v.All(str),
            # Support 0% to 200% by 10
            v.Required(
                'valueFontSize', default='80%'): v.All(
                    v.Match(r'^[1-9]?[0]{1}%$|^1[0-9]?[0]{1}%$|^200%$')),
            v.Required('valueName', default='avg'): v.Any(
                'avg', 'current', 'max', 'min', 'total'),
            v.Optional('datasource'): v.All(str),
            v.Optional('decimals'): v.All(int, v.Range(min=0, max=12)),
            v.Optional('hideTimeOverride'): v.All(bool),
            v.Optional('timeFrom'): v.All(v.Match(r'[1-9]+[0-9]*[smhdw]')),
            v.Optional('timeShift'): v.All(v.Match(r'[1-9]+[0-9]*[smhdw]')),
        }
        singlestat.update(self.base)
        return v.Schema(singlestat)
