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


class Annotations(object):

    def get_schema(self):
        list = {
            v.Required('datasource'): v.All(str),
            v.Required('enable'): v.All(bool),
            v.Required('expr'): v.All(str),
            v.Required('hide'): v.All(bool),
            v.Required('name'): v.All(str),
            v.Optional('limit'): int,
            v.Optional('titleFormat'): v.All(str),
        }

        schema = v.Schema({
            v.Optional('annotations'): {"list": [list]},
        })
        return schema
