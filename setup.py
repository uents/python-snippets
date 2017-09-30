# -*- coding: utf-8 -*-
"""setup

"""

import setuptools

setuptools.setup(
    name='my_utils',
    version='0.0.1',
    packages=[
        'my_utils.lib.app',
        'my_utils.lib.logger',
        'my_utils.lib.redis_accessor'
    ]
)
