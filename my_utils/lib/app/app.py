# -*- coding: utf-8 -*-
"""app

Application common process
"""


def main(logger=None):
    """main function decorator"""
    def _decorator(func):
        def _decorated_func(*args, **kwargs):
            system_exit = False
            status_code = 1
            logger.process_start()
            try:
                func(*args, **kwargs)
                status_code = 0
            except SystemExit as exc:
                system_exit = True
                status_code = 0 if exc.code == 0 else 1
                if status_code == 1:
                    raise
            finally:
                logger.process_end(status_code, system_exit)
                exit(status_code)

        return _decorated_func
    return _decorator
