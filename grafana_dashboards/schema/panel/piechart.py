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


class PieChart(Base):
    def get_schema(self):
        reduceOptions = {
            v.Required("values", default=False): v.All(bool),
            v.Required("calcs", default=["last"]): v.All(list),
            v.Required("fields", default=""): v.Any(str),
        }

        color = {
            v.Required("fixedColor", default="dark-red"): v.Any(str),
            v.Required("mode", default="palette-classic"): v.Any(str),
        }

        defaults = {
            v.Optional("color"): v.All(color),
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

        pie_chart = {
            v.Required("targets", default=[]): v.All(list),
            v.Required("fieldConfig"): v.All(fieldConfig),
            v.Optional("options"): v.All(options),
            v.Optional("datasource"): v.All(str),
        }
        pie_chart.update(self.base)
        return v.Schema(pie_chart)
