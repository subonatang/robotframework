# Automatically generated by 'package.py' script.

VERSION = 'trunk'
RELEASE = '20090419'
TIMESTAMP = '20090419-030634'

def get_version(sep=' '):
    if RELEASE == 'final':
        return VERSION
    return VERSION + sep + RELEASE

if __name__ == '__main__':
    import sys
    print get_version(*sys.argv[1:])
