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


class Base(object):

    def __init__(self):
        self.base = {
            v.Required('name'): v.All(str, v.Length(min=1)),
            v.Required('type'): v.Any('query', 'interval'),
        }

    def get_schema(self):
        return v.Schema(self.base, extra=True)
