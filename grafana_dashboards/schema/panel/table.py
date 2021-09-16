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


class Table(Base):
    def get_schema(self):
        style = {
            v.Optional("alias"): v.All(str),
            v.Optional("align"): v.All(str),
            v.Required("colors", default=[]): v.All(list),
            v.Optional("dateFormat"): v.All(str),
            v.Optional("decimals"): v.All(int),
            v.Optional("mappingType"): v.All(int),
            v.Optional("pattern"): v.All(str),
            v.Optional("type"): v.All(str),
            v.Optional("unit"): v.All(str),
        }
        styles = [style]

        sort = {
            v.Optional("col"): v.All(int),
            v.Required("desc", default=True): v.All(bool),
        }

        table = {
            v.Optional("fontSize"): v.All(str),
            v.Optional("pageSize"): v.All(int),
            v.Required("scroll", default=False): v.All(bool),
            v.Optional("styles"): v.All(styles, v.Length(min=1)),
            v.Required("showHeader", default=False): v.All(bool),
            v.Optional("transform"): v.All(str),
            v.Optional("type"): v.All(str),
            v.Required("targets", default=[]): v.All(list),
            v.Required("columns", default=[]): v.All(list),
            v.Optional("datasource"): v.All(str),
            v.Optional("sort"): v.All(sort),
        }
        table.update(self.base)
        return v.Schema(table , extra=True)
