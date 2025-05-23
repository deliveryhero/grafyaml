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

from grafana_dashboards.schema.panel import Panel
from grafana_dashboards.schema.panel.base import Base


class Row(Base):
    def get_schema(self):
        row = {
            v.Required("title"): v.All(str, v.Length(min=1)),
            v.Required("type", default="row"): "row",
            v.Required("collapsed", default=True): bool,
            v.Optional("repeat"): v.All(str, v.Length(min=1)),
            v.Optional("repeatDirection"): v.All(str, v.Length(min=1)),
        }
        panel = Panel(usingNewSchema=True).get_schema()
        row.update(panel.schema)
        return v.Schema(row)
