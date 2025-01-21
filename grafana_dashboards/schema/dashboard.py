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

from grafana_dashboards.schema.links import Links
from grafana_dashboards.schema.annotations import Annotations
from grafana_dashboards.schema.row import Row as DeprecatedRow
from grafana_dashboards.schema.panel.row import Row
from grafana_dashboards.schema.template import Template
from grafana_dashboards.schema.panel import Panel


class Dashboard(object):
    def get_schema(self):
        dashboard = {
            v.Required("timezone", default="utc"): v.Any("browser", "utc"),
            v.Required("title"): v.All(str, v.Length(min=1)),
            v.Optional("id"): int,
            v.Optional("uid"): v.All(str, v.Length(max=40)),
            v.Optional("sharedCrosshair"): bool,
            v.Optional("editable"): bool,
            v.Optional("tags"): [v.Any(str, v.Length(min=1))],
            v.Optional("time"): {
                v.Required("from"): v.Any(v.Datetime(), str),
                v.Required("to"): v.Any(v.Datetime(), str),
            },
        }
        links = Links().get_schema()
        dashboard.update(links.schema)
        deprecated_rows = DeprecatedRow().get_schema()
        dashboard.update(deprecated_rows.schema)

        row = Row().get_schema()
        callable_panel_validator = Panel(usingNewSchema=True).validate_individually
        # Accepts both (new) row and non-row panel
        # i.e. accepts panels outside of rows
        dashboard.update(
            {
                v.Required("panels", default=[]): [
                    v.Any(row, callable_panel_validator)
                ],
            }
        )

        templating = Template().get_schema()
        dashboard.update(templating.schema)
        annotations = Annotations().get_schema()
        dashboard.update(annotations.schema)

        return dashboard
