import unittest

from codalab.lib.server_util import *

import time


class ServerUtilTest(unittest.TestCase):
    def test_rate_limit_not_exceeded(self):
        sentinel = 23948

        @rate_limited(3600)
        def limited_function(arg):
            return arg

        for _ in xrange(3600):
            self.assertEqual(limited_function(sentinel), sentinel)

        # After one second, should recover credit for at least another call
        time.sleep(1)
        self.assertEqual(limited_function(sentinel), sentinel)

    def test_rate_limit_exceeded(self):
        @rate_limited(10)
        def limited_function():
            pass

        self.assertRaises(RateLimitExceededError,
                          lambda: [limited_function() for _ in xrange(11)])
