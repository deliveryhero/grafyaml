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


class Text(Base):

    def get_schema(self):
        text = {
            v.Required('content'): v.All(str),
            v.Required('mode', default='markdown'): v.Any(
                'html', 'markdown', 'text'),
            v.Optional('style'): dict(),
        }
        text.update(self.base)
        return v.Schema(text)
