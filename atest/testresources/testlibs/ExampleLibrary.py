import sys
import time
import exceptions

from robot import utils

from objecttoreturn import ObjectToReturn


class ExampleLibrary:

    def print_(self, msg, stream='stdout'):
        """Print given message to selected stream (stdout or stderr)"""
        out_stream = getattr(sys, stream)
        out_stream.write(msg)

    def print_n_times(self, msg, count, delay=0):
        """Print given message n times"""
        for i in range(int(count)):
            print msg
            self._sleep(delay)

    def print_many(self, *msgs):
        """Print given messages"""
        for msg in msgs:
            print msg,
        print

    def print_to_stdout_and_stderr(self, msg):
        sys.stdout.write('stdout: ' + msg)
        sys.stderr.write('stderr: ' + msg)

    def single_line_doc(self):
        """One line keyword documentation."""
        pass

    def multi_line_doc(self):
        """Only the first line of a multi line keyword doc should be logged.

        Thus for example this text here should not be there
        and neither should this.
        """
        pass

    def exception(self, name, msg=""):
        """Raise exception with given name and message"""
        exception = getattr(exceptions, name)
        raise exception, msg

    def external_exception(self, name, msg):
        ObjectToReturn('failure').exception(name, msg)

    def return_string_from_library(self,string='This is a string from Library'):
        return string

    def return_list_from_library(self, *args):
        return list(args)

    def return_three_strings_from_library(self, one='one', two='two', three='three'):
        return one, two, three

    def return_object(self, name='<noname>'):
        return ObjectToReturn(name)

    def check_object_name(self, object, name):
        assert object.name == name, '%s != %s' % (object.name, name)

    def set_object_name(self, object, name):
        object.name = name

    def set_attribute(self, name, value):
        setattr(self, utils.normalize(name), utils.normalize(value))

    def get_attribute(self, name):
        return getattr(self, utils.normalize(name))

    def check_attribute(self, name, expected):
        try:
            actual = getattr(self, utils.normalize(name))
        except AttributeError:
            raise AssertionError, "Attribute '%s' not set" % name
        if not utils.eq(actual, expected):
            raise AssertionError, "Attribute '%s' was '%s', expected '%s'" \
                    % (name, actual, expected)

    def check_attribute_not_set(self, name):
        if hasattr(self, utils.normalize(name)):
            raise AssertionError, "Attribute '%s' should not be set" % name

    def backslashes(self, count=1):
        return '\\' * int(count)

    def read_and_log_file(self, path, binary=False):
        mode = binary and 'rb' or 'r'
        _file = open(path, mode)
        print _file.read()
        _file.close()

    def print_control_chars(self):
        print '\033[31mRED\033[m\033[32mGREEN\033[m'

    def long_message(self, line_length, line_count, chars='a'):
        line_length = int(line_length)
        line_count = int(line_count)
        msg = chars*line_length + '\n'
        print msg*line_count

    def loop_forever(self, no_print=False):
        i = 0
        while True:
            i += 1
            self._sleep(1)
            if not no_print:
                print 'Looping forever: %d' % i

    def write_to_file_after_sleeping(self, path, sec, msg=None):
        f = open(path, 'w')
        self._sleep(sec)
        if msg is None:
            msg = 'Slept %s seconds' % sec
        f.write(msg)
        f.close()

    def sleep_without_logging(self, timestr):
        seconds = utils.timestr_to_secs(timestr)
        self._sleep(seconds)

    def _sleep(self, seconds):
        endtime = time.time() + float(seconds)
        while True:
            remaining = endtime - time.time()
            if remaining <= 0:
                break
            time.sleep(min(remaining, 0.5))

    def return_custom_iterable(self, *values):
        return _MyIterable(*values)

    def return_list_subclass(self, *values):
        return _MyList(values)

    def return_unrepresentable_objects(self):
        class FailiningStr(object):
            def __str__(self): raise RuntimeError
            def __unicode__(self): raise UnicodeError()
        class FailiningUnicode(object):
            def __unicode__(self): raise RuntimeError
        return FailiningStr(), FailiningUnicode()


class _MyIterable(object):
    def __init__(self, *values):
        self._list = list(values)
    def __iter__(self):
        return iter(self._list)


class _MyList(list):
    pass
