# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import os.path
import re
import subprocess
import sys
import unittest


fixture = os.path.join(os.path.dirname(__file__), 'fixture')
check_zopetestrunner = os.path.join(fixture, 'check_zopetestrunner.py')

logfile_pattern = re.compile(r'check_testrunner\.[^\.]+\.log')


def normalize_logfile(out):
    return logfile_pattern.sub('check_testrunner.XXX.log', out)


class TestPlugin(unittest.TestCase):

    def test_testrunner_should_run_tests(self):
        out, _ = subprocess.Popen(
            [sys.executable, check_zopetestrunner, '--', '--path', fixture],
            stdout=subprocess.PIPE).communicate()
        self.assertTrue('run=3.0' in out)
        self.assertTrue('errors=1.0' in out)
        self.assertTrue('failures=1.0' in out)

    def test_options_left_of_dashdash_refer_to_nagios(self):
        # to make sure the option isn't simply ignored, first check that the
        # testrunner is called without any nagios-related options
        out, _ = subprocess.Popen(
            [sys.executable, check_zopetestrunner, '--'],
            stdout=subprocess.PIPE).communicate()
        self.assertTrue('run=' in out)

        out, _ = subprocess.Popen(
            [sys.executable, check_zopetestrunner, '-h', '--',
             '--path', fixture],
            stdout=subprocess.PIPE).communicate()
        # we do see the nagios help, no testing is attempted anymore
        self.assertTrue('-t TIMEOUT' in out)
        self.assertFalse('run=' in out)

    def test_options_right_of_dashdash_refer_to_testrunner(self):
        # to make sure the option isn't simply ignored, first check that the
        # testrunner attempts to run tests without any testrunner options
        out, _ = subprocess.Popen(
            [sys.executable, check_zopetestrunner, '--'],
            stdout=subprocess.PIPE).communicate()
        self.assertTrue('run=' in out)

        out, _ = subprocess.Popen(
            [sys.executable, check_zopetestrunner, '--', '-h'],
            stdout=subprocess.PIPE).communicate()
        # we don't see the nagios help, no testing is attempted anymore
        self.assertFalse('-t TIMEOUT' in out)
        self.assertFalse('run=' in out)

    def test_nagios_output_ok(self):
        out, _ = subprocess.Popen(
            [sys.executable, check_zopetestrunner, '--',
             '--path', fixture, '-t', 'foo'],
            stdout=subprocess.PIPE).communicate()
        self.assertEqual("""\
ZOPE OK | run=1.0 errors=0.0;;0 failures=0.0;;0
""", out)

    def test_nagios_output_failure(self):
        out, _ = subprocess.Popen(
            [sys.executable, check_zopetestrunner, '--',
             '--path', fixture, '-t', 'bar'],
            stdout=subprocess.PIPE).communicate()
        self.assertEqual("""\
ZOPE CRITICAL - failures value 1.0 exceeds critical range 0 | run=1.0
Test runner output logged to /tmp/check_testrunner.XXX.log | errors=0.0;;0
failures=1.0;;0
""", normalize_logfile(out))

    def test_nagios_output_error(self):
        out, _ = subprocess.Popen(
            [sys.executable, check_zopetestrunner, '--',
             '--path', fixture, '-t', 'baz'],
            stdout=subprocess.PIPE).communicate()
        self.assertEqual("""\
ZOPE CRITICAL - errors value 1.0 exceeds critical range 0 | run=1.0
Test runner output logged to /tmp/check_testrunner.XXX.log | errors=1.0;;0
failures=0.0;;0
""", normalize_logfile(out))

    def test_failures_are_logged(self):
        out, _ = subprocess.Popen(
            [sys.executable, check_zopetestrunner, '--',
             '--path', fixture, '-t', 'bar'],
            stdout=subprocess.PIPE).communicate()
        logfile = out.splitlines()[1].split()[-3]
        logged = open(logfile).read()
        self.assertTrue(re.match("""\
Running zope.testrunner.layer.UnitTests tests:
  Set up zope.testrunner.layer.UnitTests in .* seconds.


Failure in test test_bar \\(tests.TestCase\\)
Traceback \\(most recent call last\\):
.*
    raise self.failureException, msg
AssertionError

  Ran 1 tests with 1 failures and 0 errors in .* seconds.
Tearing down left over layers:
  Tear down zope.testrunner.layer.UnitTests in .* seconds.
""", logged, re.DOTALL))

    def test_errors_are_logged(self):
        out, _ = subprocess.Popen(
            [sys.executable, check_zopetestrunner, '--',
             '--path', fixture, '-t', 'baz'],
            stdout=subprocess.PIPE).communicate()
        logfile = out.splitlines()[1].split()[-3]
        logged = open(logfile).read()
        self.assertTrue(re.match("""\
Running zope.testrunner.layer.UnitTests tests:
  Set up zope.testrunner.layer.UnitTests in .* seconds.


Error in test test_baz \\(tests.TestCase\\)
Traceback \\(most recent call last\\):
.*
    raise RuntimeError
RuntimeError

  Ran 1 tests with 0 failures and 1 errors in .* seconds.
Tearing down left over layers:
  Tear down zope.testrunner.layer.UnitTests in .* seconds.
""", logged, re.DOTALL))
