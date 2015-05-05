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


class BasePanel(object):

    def validate(self, data):
        panel = {
            v.Required('editable', default=True): v.All(bool),
            v.Required('error', default=False): v.All(bool),
            v.Required('span', default=12): v.All(int, v.Range(min=0, max=12)),
            v.Required('title'): v.All(str, v.Length(min=1)),
            v.Required('type'): v.All(str),
            v.Optional('id'): int,
        }
        panel.update(self.fields)
        schema = v.Schema({
            'panels': [panel]
        })

        return schema(data)


class Dashlist(BasePanel):
    fields = {
        v.Required('limit', default=10): v.All(int),
        v.Required('mode'): v.All(str),
        v.Required('tag', default=''): v.All(str),
        v.Required('query', default=''): v.All(str),
    }


class Text(BasePanel):
    fields = {
        v.Required('content'): v.All(str),
        v.Required('mode'): v.All(str),
        v.Optional('style'): dict(),
    }
