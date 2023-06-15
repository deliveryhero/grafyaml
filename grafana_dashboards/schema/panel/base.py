# -*- coding: utf-8 -*-

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
    formats = v.Any(
        "none",
        "short",
        "percent",
        "percentunit",
        "humidity",
        "ppm",
        "dB",
        "currencyUSD",
        "currencyGBP",
        "currencyEUR",
        "currencyJPY",
        "hertz",
        "ns",
        "µs",
        "ms",
        "s",
        "m",
        "h",
        "d",
        "bits",
        "bytes",
        "kbytes",
        "mbytes",
        "gbytes",
        "decbits",
        "decbytes",
        "deckbytes",
        "decmbytes",
        "decgbytes",
        "pps",
        "bps",
        "Bps",
        "Kbits",
        "KBs",
        "Mbits",
        "MBs",
        "GBs",
        "Gbits",
        "ops",
        "rps",
        "wps",
        "iops",
        "opm",
        "rpm",
        "wpm",
        "lengthmm",
        "lengthm",
        "lengthkm",
        "lengthmi",
        "velocityms",
        "velocitykmh",
        "velocitymph",
        "velocityknot",
        "mlitre",
        "litre",
        "m3",
        "watt",
        "kwatt",
        "watth",
        "kwatth",
        "joule",
        "ev",
        "amp",
        "volt",
        "celsius",
        "farenheit",
        "kelvin",
        "pressurembar",
        "pressurehpa",
        "pressurehg",
        "pressurepsi",
        "reqps",
        "dtdurations",
    )

    datasource = {
        v.Optional("datasource"): {
            v.Optional("type"): str,
            v.Optional("uid"): str,
        },
    }

    grid_pos = {
        v.Required("gridPos"): {
            v.Required("h", default=8): v.Range(min=0, min_included=False),
            v.Required("w", default=8): v.Range(min=0, min_included=False, max=24),
            v.Required("x", default=0): v.Clamp(min=0),
            v.Required("y", default=0): v.Clamp(min=0),
            v.Optional("static"): bool,
        },
    }

    options_with_tooltip = {
        v.Optional("tooltip"): {
            v.Required("mode"): v.Any("single", "multi", "none"),
            v.Required("sort"): v.Any("asc", "desc", "none"),
        },
    }

    options_with_legend = {
        v.Optional("legend"): {
            v.Required("displayMode"): v.Any("list", "table", "hidden"),
            v.Required("placement"): v.Any("bottom", "right"),
            v.Optional("asTable"): bool,
            v.Optional("isVisible"): bool,
            v.Optional("showLegend"): bool,
            v.Optional("sortBy"): str,
            v.Optional("sortDesc"): bool,
            v.Required("calcs", default=[]): [str],
        },
    }

    options_with_text_formatting = {
        v.Optional("text"): {
            v.Optional("titleSize"): v.Number(),
            v.Optional("valueSize"): v.Number(),
        },
    }

    def __init__(self, usingNewSchema=False):
        self.base = {
            v.Required("editable", default=True): v.All(bool),
            v.Required("error", default=False): v.All(bool),
            v.Required("span", default=12): v.All(int, v.Range(min=0, max=12)),
            v.Required("title"): v.All(str, v.Length(min=1)),
            v.Required("type"): v.Any(
                "dashlist",
                "graph",
                "logs",
                "singlestat",
                "text",
                "stat",
                "table",
                "bargauge",
                "timeseries",
                "piechart",
                "state-timeline",
            ),
            v.Optional("id"): int,
            v.Optional("format"): v.Any(self.formats, v.Length(min=1)),
            v.Optional("transparent"): v.All(bool),
            v.Optional("height"): v.All(int),
            v.Optional("description"): v.All(str),
        }

        if usingNewSchema:
            self.base.update(__class__.grid_pos)
            del self.base["span"], self.base["editable"], self.base["error"]

    def get_schema(self):
        return v.Schema(self.base, extra=True)
