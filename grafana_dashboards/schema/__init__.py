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

from grafana_dashboards.schema.dashboard import Dashboard
from grafana_dashboards.schema.datasource import Datasource
from grafana_dashboards.schema.permissions import Permissions


class Schema(object):
    def validate(self, data):
        dashboard = Dashboard().get_schema()
        datasource = Datasource().get_schema()
        permissions = Permissions().get_schema()
        schema = v.Schema(
            {
                v.Optional("dashboard"): dashboard,
                v.Optional("datasource"): datasource,
                v.Optional("permissions"): permissions,
            }
        )

        compiled: dict = schema(data)

        if "dashboard" not in compiled:
            return compiled

        # FIXME: Only temporarily allow the old schema during transition period
        if len(compiled["dashboard"]["rows"]) > 0:
            del compiled["dashboard"]["panels"]
        else:
            del compiled["dashboard"]["rows"]

        return compiled
