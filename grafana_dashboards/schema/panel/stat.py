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


class Stat(Base):
    def get_schema(self):
        reduceOptions = {
            v.Required("values", default=False): v.All(bool),
            v.Required("calcs", default=["last"]): v.All(list),
            v.Required("fields", default=""): v.Any(str),
        }

        thresholds = {
            v.Required("steps"): v.All(list),
            v.Required("mode", default="absolute"): v.Any(str),
        }

        defaults = {
            v.Required("unit", default="short"): Base.formats,
            v.Required("NoneValueMode", default="connected"): v.Any(str),
            v.Required("thresholds"): v.All(thresholds),
            v.Optional("decimals"): v.All(int),
            v.Optional("mappings", default=[]): v.All(list),
            v.Optional("color"): v.All(dict),
        }

        fieldConfig = {
            v.Required("defaults"): v.All(defaults),
            v.Required("overrides", default=[]): v.All(list),
        }

        options = {
            v.Required("orientation"): v.Any(str),
            v.Required("textMode"): v.Any(str),
            v.Required("colorMode"): v.Any(str),
            v.Required("graphMode"): v.Any(str),
            v.Required("justifyMode"): v.Any(str),
            v.Optional("reduceOptions"): v.All(reduceOptions),
        }

        grid_pos = {
            v.Required("h"): v.Any(int),
            v.Required("w"): v.Any(int),
            v.Required("x"): v.Any(int),
            v.Required("y"): v.Any(int),
        }

        stat = {
            v.Required("targets", default=[]): v.All(list),
            v.Required("fieldConfig"): v.All(fieldConfig),
            v.Optional("options"): v.All(options),
            v.Optional("datasource"): v.All(str),
            v.Optional("timeFrom"): v.All(v.Match(r"[1-9]+[0-9]*[smhdw]")),
            v.Optional("timeShift"): v.All(v.Match(r"[1-9]+[0-9]*[smhdw]")),
            v.Optional("maxDataPoints"): v.All(int),
            v.Optional("hideTimeOverride"): v.All(bool),
            v.Optional("gridPos"): v.All(grid_pos),
        }
        stat.update(self.base)
        return v.Schema(stat, extra=True)
