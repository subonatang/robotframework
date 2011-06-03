from __future__ import with_statement
import StringIO
import json
import unittest
import xml.sax as sax

from resources import GOLDEN_OUTPUT, GOLDEN_JS
from robot.serializing.jsparser import _RobotOutputHandler, Context, parse_js, json_dump
from robot.utils.asserts import assert_equals

class TestJsSerializer(unittest.TestCase):

    def setUp(self):
        self._context = Context()
        self._handler = _RobotOutputHandler(self._context)

    def test_message_xml_parsing(self):
        data_model = self._get_data_model('<msg timestamp="20110531 12:48:09.088" level="FAIL">AssertionError</msg>')
        assert_equals(data_model._basemillis, 1306835289088)
        assert_equals(data_model._robot_data, [0, 'F', 1])
        assert_equals(data_model._texts, ['*', '*AssertionError'])

    def test_status_xml_parsing(self):
        data_model = self._get_data_model('<status status="PASS" endtime="20110531 12:48:09.042" starttime="20110531 12:48:09.000"></status>')
        assert_equals(data_model._basemillis, 1306835289000)
        assert_equals(data_model._robot_data, ['P',0,42])
        assert_equals(data_model._texts, ['*'])

    def test_tags_xml_parsing(self):
        tags_xml = """
        <tags>
            <tag>someothertag</tag>
            <tag>sometag</tag>
        </tags>
        """
        data_model = self._get_data_model(tags_xml)
        assert_equals(data_model._robot_data, [1, 2])
        assert_equals(data_model._texts, ['*', '*someothertag', '*sometag'])

    def test_arguments_xml_parsing(self):
        arguments_xml = """
        <arguments>
            <arg>${arg}</arg>
            <arg>${level}</arg>
        </arguments>
        """
        data_model = self._get_data_model(arguments_xml)
        assert_equals(data_model._robot_data, 1)
        assert_equals(data_model._texts, ['*', '*${arg}, ${level}'])

    def test_keyword_xml_parsing(self):
        keyword_xml = """
        <kw type="teardown" name="BuiltIn.Log" timeout="">
            <doc>Logs the given message with the given level.</doc>
            <arguments>
                <arg>keyword teardown</arg>
            </arguments>
            <msg timestamp="20110531 12:48:09.070" level="WARN">keyword teardown</msg>
            <status status="PASS" endtime="20110531 12:48:09.071" starttime="20110531 12:48:09.069"></status>
        </kw>
        """
        self._context.start_suite('suite')
        data_model = self._get_data_model(keyword_xml)
        assert_equals(data_model._basemillis, 1306835289070)
        assert_equals(data_model._robot_data, ['teardown', 1, 0, 2, 3, [0, "W", 3], ["P", -1, 2]])
        assert_equals(data_model._texts, ['*', '*BuiltIn.Log', '*Logs the given message with the given level.', '*keyword teardown'])
        assert_equals(self._context.link_to([0, "W", 3]), "keyword_suite.0")

    def test_test_xml_parsing(self):
        test_xml = """
        <test name="Test" timeout="">
            <doc></doc>
            <kw type="kw" name="Log" timeout="">
                <doc>Logging</doc>
                <arguments>
                    <arg>simple</arg>
                </arguments>
                <msg timestamp="20110601 12:01:51.353" level="INFO">simple</msg>
                <status status="PASS" endtime="20110601 12:01:51.353" starttime="20110601 12:01:51.353"></status>
            </kw>
            <tags>
            </tags>
            <status status="PASS" endtime="20110601 12:01:51.354" critical="yes" starttime="20110601 12:01:51.353"></status>
        </test>
        """
        self._context.start_suite('SuiteName')
        data_model = self._get_data_model(test_xml)
        assert_equals(data_model._basemillis, 1306918911353)
        assert_equals(data_model._robot_data, ['test', 1, 0, 'Y', 0, ['kw', 2, 0, 3, 4, [0, 'I', 4], ['P', 0, 0]], [], ['P', 0, 1]])
        assert_equals(data_model._texts, ['*', '*Test', '*Log', '*Logging', '*simple'])

    def test_suite_xml_parsing(self):
        suite_xml = """<suite source="/tmp/verysimple.txt" name="Verysimple">
                    <doc></doc>
                    <metadata></metadata>
                    <test name="Test" timeout="">
                        <doc></doc>
                        <kw type="kw" name="BuiltIn.Log" timeout="">
                            <doc>Logs the given message with the given level.</doc>
                            <arguments><arg>simple</arg></arguments>
                            <msg timestamp="20110601 12:01:51.353" level="WARN">simple</msg>
                            <status status="PASS" endtime="20110601 12:01:51.353" starttime="20110601 12:01:51.353"></status>
                        </kw>
                        <tags></tags>
                        <status status="PASS" endtime="20110601 12:01:51.354" critical="yes" starttime="20110601 12:01:51.353"></status>
                    </test>
                    <status status="PASS" endtime="20110601 12:01:51.354" starttime="20110601 12:01:51.329"></status>
                    </suite>"""
        data_model = self._get_data_model(suite_xml)
        assert_equals(data_model._basemillis, 1306918911353)
        assert_equals(data_model._robot_data, ['suite', '/tmp/verysimple.txt', 'Verysimple',
                                               0, {},
                                                ['test', 1, 0, 'Y', 0,
                                                    ['kw', 2, 0, 3, 4, [0, 'W', 4], ['P', 0, 0]], [], ['P', 0, 1]],
                                               ['P', -24, 25], [1, 1, 1, 1]])
        assert_equals(data_model._texts, ['*', '*Test', '*BuiltIn.Log', '*Logs the given message with the given level.', '*simple'])
        assert_equals(self._context.link_to([0, 'W', 4]), 'keyword_Verysimple.Test.0')

    def test_metadata_xml_parsing(self):
        meta_xml = """<metadata>
                        <item name="meta">&lt;b&gt;escaped&lt;/b&gt;</item>
                        <item name="version">alpha</item>
                      </metadata>"""
        data_model = self._get_data_model(meta_xml)
        assert_equals(data_model._robot_data, {'meta':1, 'version':2})
        assert_equals(data_model._texts, ['*', '*<b>escaped</b>', '*alpha'])

    def test_statistics_xml_parsing(self):
        statistics_xml = """
        <statistics>
            <total>
                <stat fail="4" doc="" pass="0">Critical Tests</stat>
                <stat fail="4" doc="" pass="0">All Tests</stat>
            </total>
            <tag>
                <stat info="" fail="1" pass="0" links="" doc="">someothertag</stat>
                <stat info="" fail="1" pass="0" links="" doc="">sometag</stat>
            </tag>
            <suite>
                <stat fail="4" doc="Data" pass="0">Data</stat>
                <stat fail="1" doc="Data.All Settings" pass="0">Data.All Settings</stat>
                <stat fail="3" doc="Data.Failing Suite" pass="0">Data.Failing Suite</stat>
            </suite>
        </statistics>
        """
        data_model = self._get_data_model(statistics_xml)
        assert_equals(data_model._robot_data, [[['Critical Tests', 0, 4, '', '', ''],
            ['All Tests', 0, 4, '', '', '']],
            [['someothertag', 0, 1, '', '', ''],
                ['sometag', 0, 1, '', '', '']],
            [['Data', 0, 4, 'Data', '', ''],
                ['Data.All Settings', 0, 1, 'Data.All Settings', '', ''],
                ['Data.Failing Suite', 0, 3, 'Data.Failing Suite', '', '']]])
        assert_equals(data_model._texts, ['*'])

    def test_errors_xml_parsing(self):
        errors_xml = """
        <errors>
            <msg timestamp="20110531 12:48:09.078" level="ERROR">Invalid syntax in file '/tmp/data/failing_suite.txt' in table 'Settings': Resource file 'nope' does not exist.</msg>
        </errors>
        """
        data_model = self._get_data_model(errors_xml)
        assert_equals(data_model._basemillis, 1306835289078)
        assert_equals(data_model._robot_data, [[0, 'E', 1]])
        assert_equals(data_model._texts, ['*', "*Invalid syntax in file '/tmp/data/failing_suite.txt' in table 'Settings': Resource file 'nope' does not exist."])

    def test_json_dump_string(self):
        string = u'string\u00A9\v\\\'\"\r\b\t\0\n\fjee'
        for i in range(1024):
            string += unichr(i)
        buffer = StringIO.StringIO()
        json_dump(string, buffer)
        expected = StringIO.StringIO()
        json.dump(string, expected)
        self._assert_long_equals(buffer.getvalue(), expected.getvalue())

    def test_json_dump_integer(self):
        buffer = StringIO.StringIO()
        json_dump(12, buffer)
        assert_equals('12', buffer.getvalue())

    def test_json_dump_list(self):
        buffer = StringIO.StringIO()
        json_dump([1,2,3, 'hello', 'world'], buffer)
        assert_equals('[1,2,3,"hello","world"]', buffer.getvalue())

    def test_json_dump_dictionary(self):
        buffer = StringIO.StringIO()
        json_dump({'key':1, 'hello':'world'}, buffer)
        assert_equals('{"hello":"world","key":1}', buffer.getvalue())

    def _get_data_model(self, xml_string):
        sax.parseString(xml_string, self._handler)
        return self._handler.datamodel


    def test_golden_js_generation(self):
        buffer = StringIO.StringIO()
        parse_js(GOLDEN_OUTPUT, buffer)
        with open(GOLDEN_JS, 'r') as expected:
            self._assert_long_equals(buffer.getvalue(), expected.read())

    def _assert_long_equals(self, given, expected):
        if (given!=expected):
            for index, char in enumerate(given):
                if index >= len(expected):
                    raise AssertionError('Expected is shorter than given string. Ending that was missing %s' % given[index:])
                if char != expected[index]:
                    raise AssertionError("Given and expected not equal ('%s' != '%s') at index %s.\n'%s' !=\n'%s'" %
                                         (char, expected[index], index, self._snippet(index, given), self._snippet(index, expected)))
            if len(expected) > len(given):
                raise AssertionError('Expected is longer than given string. Ending that was missing %s' % expected[len(given)-1:])

    def _snippet(self, index, string):
        start = max(0, index-20)
        start_padding = '' if start==0 else '...'
        end = min(len(string), index+20)
        end_padding = '' if end==0 else '...'
        return start_padding+string[start:end]+end_padding
