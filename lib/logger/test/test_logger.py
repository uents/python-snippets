# -*- coding: utf-8 -*-
"""logger unittest

Logger class unittest
"""

import sys
import os
import logging
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..', '..', '..'))
import lib.logger.logger as log
print(dir(log))

_LEVEL = log.LOGGING_LEVEL


class TestLogger(unittest.TestCase):
    """Logger unittest"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_name(self):
        """logger name"""
        logger = log.Logger()
        with self.assertLogs(logger._logger, level=_LEVEL) as context:
            logger.info('ora !')
            _, name, _ = context.output[0].split(':', 2)
        self.assertRegex(name, '/(.+/)*(.+).py?$')
        print(name)

    def test_name_with_unique_id(self):
        """logger name with unique id"""
        logger = log.Logger(unique_id=123)
        with self.assertLogs(logger._logger, level=_LEVEL) as context:
            logger.info('ora !')
            _, name, _ = context.output[0].split(':', 2)
        self.assertRegex(name, '/(.+/)*(.+).py(_[0-9]*)?$')
        print(name)

    def test_critical(self):
        """critical message (with traceback)"""
        logger = log.Logger()
        with self.assertLogs(logger._logger, level=_LEVEL) as context:
            try:
                _ = 1 / 0
            except ZeroDivisionError:
                logger.critical('%s' % 'クリティカル')
                level, _, message = context.output[0].split(':', 2)
                _, _, traceback = context.output[1].split(':', 2)
            finally:
                self.assertEqual(level, 'CRITICAL')
                self.assertRegex(message, 'クリティカル$')
                self.assertRegex(traceback, 'Traceback \\(most recent call last\\)')
                print(message)
                print(traceback)

    def test_error(self):
        """error message"""
        logger = log.Logger()
        with self.assertLogs(logger._logger, level=_LEVEL) as context:
            logger.error('%s %s %s', 'エラー', '！', '！')
            level, _, message = context.output[0].split(':', 2)
        self.assertEqual(level, 'ERROR')
        self.assertRegex(message, 'エラー ！ ！$')
        print(message)

    def test_info(self):
        """info message"""
        logger = log.Logger()
        with self.assertLogs(logger._logger, level=_LEVEL) as context:
            logger.info('インフォ')
            level, _, message = context.output[0].split(':', 2)
        self.assertEqual(level, 'INFO')
        self.assertRegex(message, 'インフォ$')
        print(message)

    def test_info_with_trace(self):
        """info message with call trace"""
        logger = log.Logger(trace=True)
        with self.assertLogs(logger._logger, level=_LEVEL) as context:
            logger.info('%s %s', 'イン', 'フォ')
            level, _, message = context.output[0].split(':', 2)
        self.assertEqual(level, 'INFO')
        self.assertRegex(message, 'イン フォ ((.*):[0-9]*:(.*))$')
        print(message)

    @unittest.skipIf(_LEVEL > logging.DEBUG, 'not supported logging level')
    def test_debug(self):
        """debug message"""
        logger = log.Logger()
        with self.assertLogs(logger._logger, level=_LEVEL) as context:
            logger.debug('{}'.format('デバッグ'))
            level, _, message = context.output[0].split(':', 2)
        self.assertEqual(level, 'DEBUG')
        self.assertRegex(message, 'デバッグ$')
        print(message)


if __name__ == '__main__':
    unittest.main(verbosity=2)
