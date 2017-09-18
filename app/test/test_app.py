# -*- coding: utf-8 -*-
"""app unittest

Unittest for application common process
"""

import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..', '..'))
import app.app as app
import logger.logger as log

logger = log.Logger()


@app.main(logger=logger)
def main():
    """normal process"""
    logger.info('main')


@app.main(logger=logger)
def main_with_exit():
    """normal process with exit"""
    logger.info('main with exit')
    exit(0)


@app.main(logger=logger)
def main_with_error():
    """error process with exit"""
    logger.info('main with error')
    exit(1)


@app.main(logger=logger)
def main_with_exception():
    """error process with exception"""
    logger.info('main with exception')
    _ = 1 / 0


class TestApp(unittest.TestCase):
    """application common process unittest"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_main(self):
        try:
            main()
        except SystemExit as exc:
            self.assertEqual(0, exc.code)
        except:
            self.assertTrue(not True)

    def test_main_with_exit(self):
        try:
            main_with_exit()
        except SystemExit as exc:
            self.assertEqual(0, exc.code)
        except:
            self.assertTrue(not True)

    def test_main_with_error(self):
        try:
            main_with_error()
        except SystemExit as exc:
            self.assertEqual(1, exc.code)
        except:
            self.assertTrue(not True)

    def test_main_with_exception(self):
        try:
            main_with_exception()
        except SystemExit as exc:
            self.assertEqual(1, exc.code)
        except:
            self.assertTrue(not True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
