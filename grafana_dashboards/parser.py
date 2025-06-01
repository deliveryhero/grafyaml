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
import logging
import yaml

from slugify import slugify

from grafana_dashboards.schema import Schema
from typing import Dict, Any, Tuple

LOG = logging.getLogger(__name__)


class YamlParser(object):
    def __init__(self):
        self.data = {}

    def get_dashboard(self, slug):
        data = self.data.get("dashboard", {}).get(slug, None)
        md5 = self._generate_md5(data)
        LOG.debug("Dashboard %s: %s" % (slug, md5))

        return data, md5

    def get_datasource(self, slug: str) -> Tuple[Dict[str, Any], str]:
        data = self.data.get("datasource", {}).get(slug, None)
        md5 = self._generate_md5(data)
        LOG.debug("Datasource %s: %s" % (slug, md5))

        return data, md5

    def get_permissions(self, slug: str) -> Dict[str, Any]:
        data = self.data.get("permissions", {}).get(slug, None)
        LOG.debug("Datasource %s" % (slug))
        return data

    def parse(self, fn):
        with io.open(fn, "r", encoding="utf-8") as fp:
            self.parse_fp(fp)

    def parse_fp(self, fp):
        data = yaml.safe_load(fp)
        # Since a json file is valid YAML, we just pass through
        # any JSON files
        if fp.name.endswith(".json"):
            slug = slugify(data["title"])
            if not self.data.get("dashboard"):
                self.data["dashboard"] = {}
            self.data["dashboard"][slug] = data
        else:
            result = self.validate(data)
            for section, item in result.items():
                group = self.data.get(section, {})
                # Create slug to make it easier to find dashboards.
                if section == "dashboard":
                    name = item.get("title")
                elif section == "datasource":
                    name = item.get("name")
                elif section == "permissions":
                    name = result["dashboard"].get("title")
                else:
                    raise Exception("Unknown section: %s" % section)
                slug = slugify(name)
                if slug in group:
                    raise Exception(
                        "Duplicate {0} found in '{1}: '{2}' "
                        "already defined".format(section, fp.name, name)
                    )
                group[slug] = item
                self.data[section] = group

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        schema = Schema()
        return schema.validate(data)

    def _generate_md5(self, data) -> str:
        md5 = None
        if data:
            # Sort json keys to help our md5 hash are constant.
            content = json.dumps(data, sort_keys=True)
            md5 = hashlib.md5(content.encode("utf-8")).hexdigest()
        return md5
