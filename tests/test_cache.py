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

from grafana_dashboards import cache
from tests.base import TestCase


class TestCaseCache(TestCase):

    dashboard = {
        'hello-world': '2095312189753de6ad47dfe20cbe97ec',
    }

    def test_cache_has_changed(self):
        storage = cache.Cache(self.config.get('cache', 'cachedir'))
        res = storage.has_changed(
            'hello-world', self.dashboard['hello-world'])
        self.assertTrue(res)
        storage.set('hello-world', self.dashboard['hello-world'])
        res = storage.has_changed(
            'hello-world', self.dashboard['hello-world'])
        self.assertFalse(res)

    def test_cache_disabled_has_changed(self):
        storage = cache.Cache(self.config.get('cache', 'cachedir'), False)
        res = storage.has_changed(
            'hello-world', self.dashboard['hello-world'])
        self.assertTrue(res)
        # Set a second time and confirm cache has_changed is True.
        storage.set('hello-world', self.dashboard['hello-world'])
        res = storage.has_changed(
            'hello-world', self.dashboard['hello-world'])
        self.assertTrue(res)

    def test_cache_get_empty(self):
        storage = cache.Cache(self.config.get('cache', 'cachedir'))
        self.assertEqual(storage.get('empty'), None)

    def test_cache_disabled_get_empty(self):
        storage = cache.Cache(self.config.get('cache', 'cachedir'), False)
        self.assertEqual(storage.get('empty'), None)

    def test_cache_set_multiple(self):
        storage = cache.Cache(self.config.get('cache', 'cachedir'))
        storage.set('hello-world', self.dashboard['hello-world'])
        self.assertEqual(
            storage.get('hello-world'), self.dashboard['hello-world'])
        dashboard = {
            'foobar': '14758f1afd44c09b7992073ccf00b43d'
        }
        dashboard['hello-world'] = self.dashboard['hello-world']

        storage.set('foobar', dashboard['foobar'])
        self.assertEqual(storage.get('foobar'), dashboard['foobar'])
        # Make sure hello-world is still valid.
        self.assertEqual(
            storage.get('hello-world'), self.dashboard['hello-world'])

    def test_cache_set_single(self):
        storage = cache.Cache(self.config.get('cache', 'cachedir'))
        storage.set('hello-world', self.dashboard['hello-world'])
        self.assertEqual(
            storage.get('hello-world'), self.dashboard['hello-world'])

    def test_cache_disabled_set_single(self):
        storage = cache.Cache(self.config.get('cache', 'cachedir'), False)
        storage.set('hello-world', self.dashboard['hello-world'])
        # Make sure cache is empty
        self.assertEqual(storage.get('hello-world'), None)
