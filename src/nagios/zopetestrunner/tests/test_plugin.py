# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import os.path
import subprocess
import sys
import unittest


fixture = os.path.join(os.path.dirname(__file__), 'fixture')
check_zopetestrunner = os.path.join(fixture, 'check_zopetestrunner.py')


class TestPlugin(unittest.TestCase):

    def test_testrunner_should_run_tests(self):
        out, _ = subprocess.Popen(
            [sys.executable, check_zopetestrunner, '--', '--path', fixture],
            stdout=subprocess.PIPE).communicate()
        self.assertTrue('run=2.0' in out)
        self.assertTrue('errors=0.0' in out)
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
