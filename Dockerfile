# Copyright (c) 2020 Red Hat, Inc.
# Copyright (c) 2021 Acme Gating, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM docker.io/opendevorg/python-builder:3.8 as builder

COPY . /tmp/src
RUN assemble

FROM docker.io/opendevorg/python-base:3.8

COPY --from=builder /output/ /output
RUN /output/install-from-bindep

# To use this image, you must supply GRAFANA_URL as an env var, and
# may optionally supply GRAFANA_APIKEY.
# Mount the dashboards at /grafana.

ENTRYPOINT /usr/local/bin/grafana-dashboard --debug --grafana-url="${GRAFANA_URL}" ${GRAFANA_APIKEY:+--grafana-apikey "$GRAFANA_APIKEY"} update /grafana
