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


class Heatmap(Base):
    def get_schema(self):

        cards = {
            v.Optional("cardPadding"): v.Any(None, str),
            v.Optional("cardRound"): v.Any(None, str),
        }

        color = {
            v.Optional("cardColor", default="#b4ff00"): v.All(str),
            v.Optional("colorScale", default="sqrt"): v.All(str),
            v.Optional("colorScheme", default="interpolateOranges"): v.All(str),
            v.Optional("exponent", default=0.5): v.All(float),
            v.Optional("mode", default="opacity"): v.All(str),
        }

        dataFormat = v.Any("ts", "tsbuckets")

        hideZeroBuckets = v.All(bool)

        highlightCards = v.All(bool)

        reverseYBuckets = v.All(bool)

        tooltip = {
            v.Required("show", default=True): v.All(bool),
            v.Required("showHistogram", default=True): v.All(bool),
        }

        xAxis = {
            v.Optional("show", default=True): v.All(bool),
        }

        xBucketNumber = v.Any(None, int)
        xBucketSize = v.Any(None, int)

        yAxis = {
            v.Optional("decimals"): v.All(int),
            v.Optional("format", default="short"): Base.formats,
            v.Optional("logBase", default=1): v.All(int, v.Range(min=1)),
            v.Optional("max"): v.Any(None, int),
            v.Optional("min"): v.Any(None, int),
            v.Optional("show", default=True): v.All(bool),
            v.Optional("splitFactor"): v.Any(None, str),
        }

        yBucketBound = v.Any(None, "auto")
        yBucketNumber = v.Any(None, int)
        yBucketSize = v.Any(None, int)

        legend = {
            v.Optional("alignAsTable", default=False): v.All(bool),
            v.Optional("avg", default=False): v.All(bool),
            v.Optional("current", default=False): v.All(bool),
            v.Optional("max", default=False): v.All(bool),
            v.Optional("min", default=False): v.All(bool),
            v.Optional("rightSide", default=False): v.All(bool),
            v.Optional("show", default=False): v.All(bool),
            v.Optional("total", default=False): v.All(bool),
            v.Optional("values", default=False): v.All(bool),
            v.Optional("sortDesc", default=False): v.All(bool),
            v.Optional("sort"): v.All(str),
        }

        heatmap = {
            v.Optional("cards"): v.All(cards),
            v.Optional("color"): v.All(color),
            v.Optional("dataFormat"): v.All(dataFormat),
            v.Optional("datasource"): v.All(str),
            v.Optional("hideZeroBuckets"): v.All(hideZeroBuckets),
            v.Optional("highlightCards"): v.All(highlightCards),
            v.Optional("legend"): v.All(legend),
            v.Optional("reverseYBuckets"): v.All(reverseYBuckets),
            v.Required("targets", default=[]): v.All(list),
            v.Optional("tooltip"): v.All(tooltip),
            v.Optional("xAxis"): v.All(xAxis),
            v.Optional("xBucketNumber"): v.All(xBucketNumber),
            v.Optional("xBucketSize"): v.All(xBucketSize),
            v.Optional("yAxis"): v.All(yAxis),
            v.Optional("yBucketBound"): v.All(yBucketBound),
            v.Optional("yBucketNumber"): v.All(yBucketNumber),
            v.Optional("yBucketSize"): v.All(yBucketSize),
        }
        heatmap.update(self.base)
        return v.Schema(heatmap, extra=True)
