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
    formats = v.Any(u'none', u'short', u'percent', u'percentunit',
                    u'humidity', u'ppm', u'dB', u'currencyUSD',
                    u'currencyGBP', u'currencyEUR', u'currencyJPY', u'hertz',
                    u'ns', u'µs', u'ms', u's', u'm', u'h', u'd', u'bits',
                    u'bytes', u'kbytes', u'mbytes', u'gbytes', u'decbits',
                    u'decbytes', u'deckbytes', u'decmbytes', u'decgbytes',
                    u'pps', u'bps', u'Bps', u'Kbits', u'KBs', u'Mbits',
                    u'MBs', u'GBs', u'Gbits', u'ops', u'rps', u'wps', u'iops',
                    u'opm', u'rpm', u'wpm', u'lengthmm', u'lengthm',
                    u'lengthkm', u'lengthmi', u'velocityms', u'velocitykmh',
                    u'velocitymph', u'velocityknot', u'mlitre', u'litre',
                    u'm3', u'watt', u'kwatt', u'watth', u'kwatth', u'joule',
                    u'ev', u'amp', u'volt', u'celsius', u'farenheit',
                    u'kelvin', u'pressurembar', u'pressurehpa', u'pressurehg',
                    u'pressurepsi')

    def __init__(self):
        self.base = {
            v.Required('editable', default=True): v.All(bool),
            v.Required('error', default=False): v.All(bool),
            v.Required('span', default=12): v.All(int, v.Range(min=0, max=12)),
            v.Required('title'): v.All(str, v.Length(min=1)),
            v.Required('type'): v.Any(
                'dashlist', 'graph', 'singlestat', 'text', 'row'),
            v.Optional('id'): int,
            v.Optional('format'): v.Any(self.formats, v.Length(min=1)),
            v.Optional('transparent'): v.All(bool),
        }

    def get_schema(self):
        return v.Schema(self.base, extra=True)
