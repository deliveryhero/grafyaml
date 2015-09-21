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

import hashlib
import io
import json
import yaml

from slugify import slugify

from grafana_dashboards.schema.dashboard import Dashboard


class YamlParser(object):

    def __init__(self):
        self.data = {}

    def get_dashboard(self, slug):
        data = self.data.get('dashboard', {}).get(slug, None)
        md5 = None
        if data:
            content = json.dumps(data)
            md5 = hashlib.md5(content.encode('utf-8')).hexdigest()

        return data, md5

    def parse(self, fn):
        with io.open(fn, 'r', encoding='utf-8') as fp:
            self.parse_fp(fp)

    def parse_fp(self, fp):
        data = yaml.safe_load(fp)
        result = self.validate(data)
        for item in result.items():
            group = self.data.get(item[0], {})
            # Create slug to make it easier to find dashboards.
            title = item[1]['title']
            slug = slugify(title)
            if slug in group:
                raise Exception(
                    "Duplicate dashboard found in '{0}: '{1}' "
                    "already defined".format(fp.name, title))
            group[slug] = item[1]
            self.data[item[0]] = group

    def validate(self, data):
        schema = Dashboard()
        return schema.validate(data)
