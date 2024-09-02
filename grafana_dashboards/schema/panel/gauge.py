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


class Gauge(Base):
    def get_schema(self):
        reduceOptions = {
            v.Required("values", default=False): v.All(bool),
            v.Required("calcs", default=["last"]): v.All(list),
            v.Required("fields", default=""): v.Any(str),
        }

        fieldConfigDefaults = {
            v.Optional("thresholds"): v.All(
                {v.Required("mode"): v.Any(str), v.Required("steps"): v.Any(list)}
            ),
            v.Optional("color"): v.All(
                {
                    v.Required("mode", default="palette-classic"): v.Any(str),
                    v.Required("palette", default="cool"): v.Any(str),
                }
            ),
            v.Optional("min", default="0"): v.Any(int),
            v.Optional("max", default="0"): v.Any(int),
            v.Optional("unit"): v.Any(str),
            v.Optional("links"): v.Any(list),
            v.Optional("decimal", default=2): v.Any(int),
        }

        fieldConfig = {
            v.Required("overrides", default=[]): v.All(list),
            v.Optional("defaults"): v.All(fieldConfigDefaults),
        }

        options = {
            v.Optional("reduceOptions"): v.All(reduceOptions),
            v.Optional("showThresholdLabels", default=True): v.Any(str),
            v.Optional("showThresholdMarkers", default=True): v.Any(str),
        }

        gridPos = {
            v.Required("h"): v.Any(int),
            v.Required("w"): v.Any(int),
            v.Required("x"): v.Any(int),
            v.Required("y"): v.Any(int),
        }

        bargauge = {
            v.Required("targets", default=[]): v.All(list),
            v.Optional("fieldConfig"): v.All(fieldConfig),
            v.Optional("options"): v.All(options),
            v.Optional("datasource"): v.All(str),
            v.Optional("gridPos"): v.All(gridPos),
        }
        bargauge.update(self.base)
        return v.Schema(bargauge, extra=True)
