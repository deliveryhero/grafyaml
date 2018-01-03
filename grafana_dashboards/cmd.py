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

import argparse
import logging
import os
import sys

from grafana_dashboards import __version__
from grafana_dashboards.builder import Builder
from grafana_dashboards.config import Config

LOG = logging.getLogger(__name__)


class Client(object):

    def delete(self):
        LOG.info('Deleting schema in %s', self.args.path)
        builder = Builder(self.config)
        builder.delete(self.args.path)

    def main(self):
        self.parse_arguments()
        self.setup_logging()
        self.read_config()

        self.args.func()

    def parse_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--config-file', dest='config', help='Path to a config file to '
            'use. The default file used is: /etc/grafyaml/grafyaml.conf')
        parser.add_argument(
            '--debug', dest='debug', action='store_true',
            help='Print debugging output (set logging level to DEBUG instead '
            ' of default INFO level)')
        parser.add_argument(
            '--grafana-url', dest='grafana_url', help='URL for grafana '
            'server. The default used is: http://localhost:8080')
        parser.add_argument(
            '--grafana-apikey', dest='grafana_apikey',
            help='API key to access grafana.')
        parser.add_argument(
            '--version', dest='version', action='version',
            version=__version__, help="show "
            "program's version number and exit")

        subparsers = parser.add_subparsers(
            title='commands')

        parser_delete = subparsers.add_parser('delete')
        parser_delete.add_argument(
            'path', help='colon-separated list of paths to YAML files or'
            ' directories')
        parser_delete.set_defaults(func=self.delete)

        parser_update = subparsers.add_parser('update')
        parser_update.add_argument(
            'path', help='colon-separated list of paths to YAML files or'
            ' directories')
        parser_update.set_defaults(func=self.update)

        parser_validate = subparsers.add_parser('validate')
        parser_validate.add_argument(
            'path', help='colon-separated list of paths to YAML files or'
            ' directories')
        parser_validate.set_defaults(func=self.validate)

        self.args = parser.parse_args()

    def read_config(self):
        self.config = Config()
        if self.args.config:
            fp = self.args.config
        else:
            fp = '/etc/grafyaml/grafyaml.conf'
        self.config.read(os.path.expanduser(fp))
        if self.args.grafana_url:
            self.config.set('grafana', 'url', self.args.grafana_url)
            LOG.debug('Grafana URL override: {}'.format(self.args.grafana_url))
        if self.args.grafana_apikey:
            self.config.set('grafana', 'apikey', self.args.grafana_apikey)
            LOG.debug('Grafana APIKey overridden')

    def setup_logging(self):
        if self.args.debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

    def update(self):
        LOG.info('Updating schema in %s', self.args.path)
        builder = Builder(self.config)
        builder.update(self.args.path)

    def validate(self):
        LOG.info('Validating schema in %s', self.args.path)
        # NOTE(pabelanger): Disable caching support by default, in an effort
        # to improve performance.
        self.config.set('cache', 'enabled', 'false')
        builder = Builder(self.config)

        try:
            builder.load_files(self.args.path)
            print('SUCCESS!')
        except Exception as e:
            print('%s: ERROR: %s' % (self.args.path, e))
            sys.exit(1)


def main():
    client = Client()
    client.main()
    sys.exit(0)
