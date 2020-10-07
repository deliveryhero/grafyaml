# Copyright 2015 IBM Corp.
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

from grafana_dashboards.schema.template.base import AUTO_INTERVAL
from grafana_dashboards.schema.template.base import Base


class Interval(Base):
    current = {
        v.Required("text"): v.All(str, v.Length(min=1)),
        v.Required("value"): v.All(str, v.Length(min=1)),
    }

    def validate_options(self, options):
        options = self._validate_options(options)

        if len(options):
            selected_options = [x for x in options if x.get("selected")]
            # If the user did not specify any selected options, mark
            # the first one as selected.
            if len(selected_options) == 0:
                options[0]["selected"] = True
            elif len(selected_options) > 1:
                raise v.Invalid("No more than one option must be selected")

        return options

    def _validate(self, data):
        # This method performs some validation but also coerces some
        # values as needed to be friendlier.

        interval = {
            v.Required("allFormat", default="glob"): v.Any("glob"),
            # This will be automatically supplied based on the options:
            v.Required("auto"): v.Any(bool),
            v.Required("auto_count", default=10): v.Any(int),
            # This will be automatically supplied based on the options:
            v.Required("current"): v.Any(self.current),
            # NOTE(jeblair): I don't know what datasource means in this context
            v.Required("datasource", default=None): v.All(None),
            v.Required("hideLabel", default=False): v.Any(bool),
            v.Required("includeAll", default=False): v.All(bool),
            v.Required("label", default=""): v.Any(str),
            v.Required("multi", default=False): v.All(bool),
            v.Required("multiFormat", default="glob"): v.Any("glob"),
            v.Required("options", default=[]): self.validate_options,
            # This will be automatically supplied based on the options:
            v.Required("query"): v.Any(str),
            # NOTE(jeblair): I don't know what refresh means in this context
            v.Required("refresh", default=False): v.All(bool),
        }
        interval.update(self.base)

        # Make sure we have the minimum we need before we start
        # messing with the data.
        rudimentary_interval_schema = {
            v.Required("options", default=[]): self.validate_options,
        }
        data = v.Schema(rudimentary_interval_schema, extra=True)(data)

        # There are some values that would be annoying to be required
        # to be included by the user because they are calculable from
        # other values, and ought to be identical.  Therefore, if they
        # are not supplied, we will calculate them for the user.
        auto = False
        selected = None
        options = data.get("options", [])
        query = []
        for option in options:
            if option["value"] == AUTO_INTERVAL:
                auto = True
            else:
                query.append(option["value"])
            if option.get("selected"):
                selected = option
        query = ",".join(query)

        # If 'auto' is not supplied, set it based on the presense of
        # an 'auto' option in the options list.
        if "auto" not in data:
            data["auto"] = auto

        # If 'current' is not supplied, set it based on which of the
        # options was marked 'selected'.
        if "current" not in data:
            if selected:
                data["current"] = dict(text=selected["text"], value=selected["value"])
            else:
                data["current"] = dict()

        # If 'query' is not supplied, compose it from the list of options.
        if "query" not in data:
            data["query"] = query

        data = v.Schema(interval)(data)
        return data

    def get_schema(self):
        return v.Schema(self._validate)
