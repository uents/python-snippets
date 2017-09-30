# -*- coding: utf-8 -*-
"""redis accessor unittest

Unittest for redis accessor class
"""

import subprocess
import unittest
import time


class TestApp(unittest.TestCase):
    """redis accessor unittest"""
    server = None

    @classmethod
    def setUpClass(cls):
        print('setUpClass')
        cls.server = subprocess.Popen(['redis-server'])
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass')
        cls.server.terminate()

    def setUp(self):
        print('setUp')

    def tearDown(self):
        print('tearDown')

    def test_hello(self):
        print('hello')

    def test_good_bye(self):
        print('good bye')


if __name__ == '__main__':
    unittest.main()
