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


class Datasource(object):

    def get_schema(self):
        datasource = {
            v.Required('access', default='direct'): v.Any('direct', 'proxy'),
            v.Required('isDefault', default=False): v.All(bool),
            v.Required('name'): v.All(str, v.Length(min=1)),
            v.Required('type', default='graphite'): v.Any('graphite',
                                                          'influxdb'),
            v.Required('url'): v.All(str, v.Length(min=1)),
            v.Optional('orgId'): int,
        }
        return datasource
