#  Copyright 2008-2012 Nokia Siemens Networks Oyj
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


class ExecutionStatus(object):

    def __init__(self, parent_status=None):
        self.parent_status = parent_status
        self.setup_failure = None
        self.test_failure = None
        self.teardown_failure = None
        self.teardown_allowed = False

    def setup_executed(self, failure=None):
        if failure:
            self.setup_failure = unicode(failure)
        self.teardown_allowed = True

    def test_failed(self, failure):
        self.test_failure = unicode(failure)

    def teardown_executed(self, failure=None):
        if failure:
            self.teardown_failure = unicode(failure)

    @property
    def message(self):
        if self.parent_status and self.parent_status.failures:
            return ParentMessageCreator(self.parent_status).create()
        return MessageCreator(self).create()

    @property
    def failures(self):
        return bool(self.parent_status and self.parent_status.failures or
                    self.setup_failure or
                    self.test_failure or
                    self.teardown_failure)


# TODO: Messages below are not identical to old run messages!!
# Remember to also update messages in SuiteTeardownFailureHandler

class MessageCreator(object):
    setup_failed = 'Setup failed:\n%s'
    teardown_failed = 'Teardown failed:\n%s'
    also_teardown_failed = '%s\n\nAlso teardown failed:\n%s'

    def __init__(self, status):
        self.setup = status.setup_failure
        self.test = status.test_failure or ''
        self.teardown = status.teardown_failure

    def create(self):
        msg = self._get_message_before_teardown()
        return self._get_message_after_teardown(msg)

    def _get_message_before_teardown(self):
        if self.setup:
            return self.setup_failed % self.setup
        return self.test

    def _get_message_after_teardown(self, msg):
        if not self.teardown:
            return msg
        if not msg:
            return self.teardown_failed % self.teardown
        return self.also_teardown_failed % (msg, self.teardown)


class ParentMessageCreator(MessageCreator):
    setup_failed = 'Parent suite setup failed:\n%s'
