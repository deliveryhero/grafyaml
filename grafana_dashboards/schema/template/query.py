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

import logging

import voluptuous as v

from grafana_dashboards.schema.template.base import Base

LOG = logging.getLogger(__name__)


class Query(Base):

    def get_schema(self):
        query = {
            v.Required('includeAll', default=False): v.All(bool),
            v.Required('multi', default=False): v.All(bool),
            v.Required('query', default=''): v.All(str),
            v.Required('refresh',
                       default=1): v.All(int, v.Range(min=0, max=2)),
            v.Optional('datasource'): v.All(str),
            v.Optional('hide'): v.All(int, v.Range(min=0, max=2)),
        }
        query.update(self.base)
        return v.Schema(query)
