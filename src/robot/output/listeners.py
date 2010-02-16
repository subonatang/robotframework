#  Copyright 2008-2009 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


import types

from robot import utils
from robot.errors import DataError
from loggerhelper import AbstractLoggerProxy
from logger import LOGGER

if utils.is_jython:
    from java.lang import Object


class Listeners:

    _start_attrs = ['doc', 'starttime', 'longname']
    _end_attrs = _start_attrs + ['endtime', 'elapsedtime', 'status', 'message']

    def __init__(self, listeners):
        self._listeners = self._import_listeners(listeners)

    def __nonzero__(self):
        return len(self._listeners) > 0

    def _import_listeners(self, listener_data):
        listeners = []
        for name, args in listener_data:
            try:
                listeners.append(_ListenerProxy(name, args))
            except:
                message, details = utils.get_error_details()
                if args:
                    name += ':' + ':'.join(args)
                LOGGER.error("Taking listener '%s' into use failed: %s"
                             % (name, message))
                LOGGER.info("Details:\n%s" % details)
        return listeners

    def start_suite(self, suite):
        for li in self._listeners:
            if li.version == 1:
                li.call_method(li.start_suite, suite.name, suite.doc)
            else:
                attrs = self._get_start_attrs(suite, [])
                li.call_method(li.start_suite, suite.name, attrs)

    def end_suite(self, suite):
        for li in self._listeners:
            if li.version == 1:
                li.call_method(li.end_suite, suite.status,
                               suite.get_full_message())
            else:
                attrs = self._get_end_attrs(suite, [],
                                            {'statistics': 'get_stat_message'})
                li.call_method(li.end_suite, suite.name, attrs)

    def start_test(self, test):
        for li in self._listeners:
            if li.version == 1:
                li.call_method(li.start_test, test.name, test.doc, test.tags)
            else:
                attrs = self._get_start_attrs(test, ['tags'])
                li.call_method(li.start_test, test.name, attrs)

    def end_test(self, test):
        for li in self._listeners:
            if li.version == 1:
                li.call_method(li.end_test, test.status, test.message)
            else:
                attrs = self._get_end_attrs(test, ['tags'])
                li.call_method(li.end_test, test.name, attrs)

    def start_keyword(self, kw):
        for li in self._listeners:
            if li.version == 1:
                li.call_method(li.start_keyword, kw.name, kw.args)
            else:
                attrs = self._get_start_attrs(kw, ['args', '-longname'])
                li.call_method(li.start_keyword, kw.name, attrs)

    def end_keyword(self, kw):
        for li in self._listeners:
            if li.version == 1:
                li.call_method(li.end_keyword, kw.status)
            else:
                attrs = self._get_end_attrs(kw, ['args', '-longname', '-message'])
                li.call_method(li.end_keyword, kw.name, attrs)

    def log_message(self, msg):
        for li in self._listeners:
            if li.version != 1:
                li.call_method(li.log_message, msg.message, msg.level)

    def message(self, msg):
        for li in self._listeners:
            if li.version != 1:
                li.call_method(li.message, msg.message, msg.level)

    def output_file(self, name, path):
        for li in self._listeners:
            li.call_method(getattr(li, '%s_file' % name.lower()), path)

    def close(self):
        for li in self._listeners:
            li.call_method(li.close)

    def _get_start_attrs(self, item, names, mapping=None):
        return self._get_attrs(item, self._start_attrs, names, mapping)

    def _get_end_attrs(self, item, names, mapping=None):
        return self._get_attrs(item, self._end_attrs, names, mapping)

    def _get_attrs(self, item, defaults, extras, mapping=None):
        names = defaults[:]
        for name in extras:
            if name.startswith('-'):
                names.remove(name[1:])
            else:
                names.append(name)
        if not mapping:
            mapping = {}
        mapping.update(dict([(n, n) for n in names]))
        attrs = {}
        for name, attr in mapping.items():
            attr = getattr(item, attr)
            if callable(attr):
                attr = attr()
            attrs[name] = attr
        return attrs


class _ListenerProxy(AbstractLoggerProxy):
    _methods = ['start_suite', 'end_suite', 'start_test', 'end_test',
                'start_keyword', 'end_keyword', 'log_message', 'message',
                'output_file', 'summary_file', 'report_file', 'log_file',
                'debug_file', 'close']

    def __init__(self, name, args):
        listener = self._import_listener(name, args)
        AbstractLoggerProxy.__init__(self, listener)
        self.name = name
        self.version = self._get_version(listener)
        self.is_java = utils.is_jython and isinstance(listener, Object)

    def _import_listener(self, name, args):
        listener, source = utils.import_(name, 'listener')
        if not isinstance(listener, types.ModuleType):
            listener = listener(*args)
        elif args:
            raise DataError("Listeners implemented as modules do not take arguments")
        LOGGER.info("Imported listener '%s' with arguments %s (source %s)"
                    % (name, utils.seq2str2(args), source))
        return listener

    def _get_version(self, listener):
        try:
            return int(getattr(listener, 'ROBOT_LISTENER_API_VERSION', 1))
        except ValueError:
            return 1

    def call_method(self, method, *args):
        if self.is_java and len(args) == 2 and isinstance(args[1], dict):
            args = (args[0], utils.dict2map(args[1]))
        try:
            method(*args)
        except:
            message, details = utils.get_error_details()
            LOGGER.error("Calling '%s' method of listener '%s' failed: %s"
                         % (method.__name__, self.name, message))
            LOGGER.info("Details:\n%s" % details)

