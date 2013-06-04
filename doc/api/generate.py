#!/usr/bin/env python

import os
import shutil
from optparse import OptionParser
from os.path import abspath, dirname, join
from subprocess import call
from sys import exit


class GenerateDocs(object):

    BUILD_DIR = abspath(dirname(__file__))
    AUTODOC_DIR = join(BUILD_DIR, 'autodoc')
    ROOT = join(BUILD_DIR, '..', '..')
    ROBOT_DIR = join(ROOT, 'src', 'robot')
    JAVA_SRC = join(ROOT, 'src', 'java')
    JAVA_TARGET = join(BUILD_DIR, '_static', 'javadoc')

    def __init__(self):
        try:
            import sphinx as _
        except ImportError:
            exit('Generating API docs requires Sphinx')
        self.options = GeneratorOptions()

    def run(self):
        self.create_autodoc()
        if self.options.also_javadoc:
            self.create_javadoc()
        orig_dir = abspath(os.curdir)
        os.chdir(self.BUILD_DIR)
        rc = call(['make', 'html'], shell=os.name == 'nt')
        os.chdir(orig_dir)
        print abspath(join(self.BUILD_DIR, '_build', 'html', 'index.html'))
        exit(rc)

    def clean_directory(self, dirname):
        if os.path.exists(dirname):
            print 'Cleaning', dirname
            shutil.rmtree(dirname)

    def create_autodoc(self):
        self.clean_directory(self.AUTODOC_DIR)
        print 'Creating autodoc'
        call(['sphinx-apidoc', '--output-dir', self.AUTODOC_DIR, '--force',
              '--no-toc', '--maxdepth', '2', self.ROBOT_DIR])

    def create_javadoc(self):
        self.clean_directory(self.JAVA_TARGET)
        print 'Creating javadoc'
        call(['javadoc', '-sourcepath', self.JAVA_SRC, '-d', self.JAVA_TARGET,
              '-notimestamp', 'org.robotframework'])


class GeneratorOptions():

    usage = """
    generate.py [options]

    This script creates API documentation from both Python and Java source code
    included in `src/python and `src/java`, respectively. Python autodocs are
    created in `doc/api/autodoc` and Javadocs in `doc/api/_static/javadoc`.

    API documentation entry point is create using Sphinx's `make html`.

    Sphinx, sphinx-apidoc and javadoc commands need to be in $PATH.
    """

    def __init__(self):
        self._parser = OptionParser(self.usage)
        self._add_parser_options()
        self._options, _ = self._parser.parse_args()
        if not self._options.also_javadoc:
           self.prompt_for_javadoc()

    @property
    def also_javadoc(self):
        return self._options.also_javadoc

    def _add_parser_options(self):
        self._parser.add_option("-j", "--also-javadoc",
            action='store_true',
            dest="also_javadoc",
            help="also generate Javadocs (off by default)"
        )

    def prompt_for_javadoc(self):
        selection = raw_input("Also generate Javadoc [Y/N] (N by default) > ")
        if len(selection) > 0 and selection[0].lower() == "y":
            self._options.also_javadoc = True


if __name__ == '__main__':
    GenerateDocs().run()
