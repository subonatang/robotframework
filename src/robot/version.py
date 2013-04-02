# Automatically generated by 'package.py' script.

import sys

VERSION = 'trunk'
RELEASE = '20130226'
TIMESTAMP = '20130226-112248'

def get_version(sep=' '):
    if RELEASE == 'final':
        return VERSION
    return VERSION + sep + RELEASE

def get_full_version(who=''):
    sys_version = sys.version.split()[0]
    version = '%s %s (%s %s on %s)' \
        % (who, get_version(), _get_interpreter(), sys_version, sys.platform)
    return version.strip()

def _get_interpreter():
    if sys.platform.startswith('java'):
        return 'Jython'
    if sys.platform == 'cli':
        return 'IronPython'
    if 'PyPy' in sys.version:
        return 'PyPy'
    return 'Python'
