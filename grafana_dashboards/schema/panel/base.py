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

    def __init__(self):
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
                "row",
                "stat",
                "table",
                "bargauge",
                "heatmap",
            ),
            v.Optional("id"): int,
            v.Optional("format"): v.Any(self.formats, v.Length(min=1)),
            v.Optional("transparent"): v.All(bool),
            v.Optional("height"): v.All(int),
            v.Optional("description"): v.All(str),
        }

    def get_schema(self):
        return v.Schema(self.base, extra=True)
