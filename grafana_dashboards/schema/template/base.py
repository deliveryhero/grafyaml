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


AUTO_INTERVAL = '$__auto_interval'
ALL_CUSTOM = '$__all'


class Base(object):
    option = {
        v.Required('text'): v.All(str, v.Length(min=1)),
        v.Required('value'): v.All(str, v.Length(min=1)),
        v.Required('selected', default=False): v.All(bool),
    }
    options = [option]

    def _validate_options(self, options):
        # Most of the time this is going to be a simple list, so if
        # the user supplied a list of strings, let's turn that into
        # the requisite list of dicts.
        try:
            v.Schema([str])(options)
            options = [dict(text=o) for o in options]
        except v.Invalid:
            pass

        # Ensure this is a list of dicts before we start messing with
        # them.
        v.Schema([dict])(options)

        # This performs some automatic cleanup to make things easier.
        for option in options:
            # Let's not make our users type "$__auto_interval".  Instead,
            # if they specify an option name of 'auto' with no value,
            # supply it for them.  NB: if a user wants 'auto' with value
            # 'foobar', they can just override this by simply including
            # 'value: foobar'.
            if option.get('text') == 'auto' and 'value' not in option:
                option['value'] = AUTO_INTERVAL

            if option.get('text') == 'all' and 'value' not in option:
                option['value'] = ALL_CUSTOM

            # Let's also not make our users type every option twice.  For
            # each option with a text entry but no value, copy the next
            # entry to that value.
            if option.get('text') and 'value' not in option:
                option['value'] = option['text']

        return v.Schema(self.options)(options)

    def __init__(self):
        self.base = {
            v.Required('name'): v.All(str, v.Length(min=1)),
            v.Required('type'): v.Any('query', 'interval', 'custom',
                                      'datasource', 'adhoc'),
        }

    def get_schema(self):
        return v.Schema(self.base, extra=True)
