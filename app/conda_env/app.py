# -*- coding: utf-8 -*-

import sys
import my_utils.lib.logger.logger as log

logger = log.Logger(file_output=False)


def main():
    logger.info(',\n'.join(sys.path))


if __name__ == '__main__':
    main()
