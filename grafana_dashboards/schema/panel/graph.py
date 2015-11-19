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
        }
        graph.update(self.base)
        return v.Schema(graph)
