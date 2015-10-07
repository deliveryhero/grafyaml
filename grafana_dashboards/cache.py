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

import logging
import os

from dogpile.cache.region import make_region

LOG = logging.getLogger(__name__)


class Cache(object):

    def __init__(self, cachedir):
        cache_dir = self._get_cache_dir(cachedir)
        self.region = make_region().configure(
            'dogpile.cache.dbm',
            arguments={
                'filename': os.path.join(cache_dir, 'cache.dbm')
            }
        )

    def get(self, title):
        res = self.region.get(title)
        return res if res else None

    def has_changed(self, title, md5):
        if self.get(title) == md5:
            return False
        return True

    def set(self, title, md5):
        self.region.set(title, md5)

    def _get_cache_dir(self, cachedir):
        path = os.path.expanduser(cachedir)
        if not os.path.isdir(path):
            os.makedirs(path)
        return path
