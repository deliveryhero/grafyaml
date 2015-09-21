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

import os

from dogpile.cache.region import make_region
from oslo_config import cfg
from oslo_log import log as logging

cache_opts = [
    cfg.StrOpt(
        'cachedir', default='~/.cache/grafyaml',
        help='Directory used by grafyaml to store its cache files.'),
    cfg.BoolOpt(
        'enabled', default=True,
        help='Maintain a special cache that contains an MD5 of every '
        'generated dashboard.'),
]
cache_group = cfg.OptGroup(
    name='cache', title='Cache options')
list_opts = lambda: [(cache_group, cache_opts), ]

CONF = cfg.CONF
CONF.register_opts(cache_opts)
CONF.register_opts(cache_opts, group='cache')

LOG = logging.getLogger(__name__)


class Cache(object):

    def __init__(self):
        if not CONF.cache.enabled:
            return

        cache_dir = self._get_cache_dir()
        self.region = make_region().configure(
            'dogpile.cache.dbm',
            arguments={
                'filename': os.path.join(cache_dir, 'cache.dbm')
            }
        )

    def get(self, title):
        if CONF.cache.enabled:
            res = self.region.get(title)
            return res if res else None
        return None

    def has_changed(self, title, md5):
        if CONF.cache.enabled and self.get(title) == md5:
            return False
        return True

    def set(self, title, md5):
        if CONF.cache.enabled:
            self.region.set(title, md5)

    def _get_cache_dir(self):
        path = os.path.expanduser(CONF.cache.cachedir)
        if not os.path.isdir(path):
            os.makedirs(path)
        return path
