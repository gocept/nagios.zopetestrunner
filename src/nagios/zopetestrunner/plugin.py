import StringIO
import nagiosplugin
import tempfile
import zope.testrunner.runner

testrunner_argv = []


class CheckZopeTestRunner(nagiosplugin.Check):

    name = 'Zope test runner check'
    version = '0.1'

    def __init__(self, optp, logger):
        super(CheckZopeTestRunner, self).__init__(optp, logger)
        self.logger = logger

    def obtain_data(self):
        sys.argv[:] = sys.argv[:1]
        self.runner = zope.testrunner.runner.Runner(testrunner_argv)
        old_stdout = sys.stdout
        sys.stdout = redirected_stdout = StringIO.StringIO()
        try:
            self.runner.run()
        finally:
            sys.stdout = old_stdout
        if self.runner.failed:
            log = tempfile.mktemp('.log', 'check_testrunner.')
            redirected_stdout.seek(0)
            open(log, 'w').write(redirected_stdout.getvalue())
            self.logger.error("Test runner output logged to %s" % log)
        self.measures = [
            nagiosplugin.Measure(u'run', float(self.runner.ran)),
            nagiosplugin.Measure(u'errors', float(len(self.runner.errors)), critical='0:0'),
            nagiosplugin.Measure(u'failures', float(len(self.runner.failures)), critical='0:0')]


def main():
    if '--' in sys.argv:
        testrunner_argv = sys.argv[sys.argv.index('--')+1:]
        sys.argv[:] = sys.argv[:sys.argv.index('--')]
    nagiosplugin.Controller(CheckZopeTestRunner)()
