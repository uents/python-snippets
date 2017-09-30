# -*- coding: utf-8 -*-
"""subprocess test

Subprocess test
"""

import sys
import os
import time
import signal
import multiprocessing as mp

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..', '..'))
import lib.logger.logger as log

logger = log.Logger(file_output=True)


def func(msg, logger):
    is_terminate = False

    def handler(signum, frame):
        nonlocal is_terminate
        is_terminate = True
        logger.info('proc terminated {}'.format(msg))
        exit(1)
#    signal.signal(signal.SIGTERM, handler)

    try:
        logger.info('{} proc start {}'.format(__name__, msg))
        time.sleep(3)
    finally:
        logger.info('proc end {}'.format(msg))


class Foo():
    def __init__(self, logger_):
        self.message = ""
        self.logger = logger_

    def update(self, message):
        logger.info(message)
        self.message = message


def update(foo, queue, message):
    logger.info(foo)
    foo.update(message)
#    queue.put(foo.message)
    queue.put(list(range(100)),


def main():
    logger.info('start')

    agents=[{'foo': Foo(logger), 'queue': mp.Queue()} for count in range(5)]
    workers=[mp.Process(target=update, args=(agent['foo'], agent['queue'], number))
               for number, agent in enumerate(agents)]
    for worker in workers:
        worker.start()

    logger.info('waiting')
    time.sleep(.5)

    for agent in agents:
        logger.info(agent['queue'].get())

    logger.info('terminate')
    for worker in workers:
        if worker.is_alive():
            logger.info('terminate: {}'.format(worker))
#            worker.terminate()
#            signal.signal(signal.SIGUSR1, _term_signal_handler)

    time.sleep(2)
    logger.info('join')
    for worker in workers:
        worker.join(.1)

    logger.info('end')


if __name__ == '__main__':
    main()
