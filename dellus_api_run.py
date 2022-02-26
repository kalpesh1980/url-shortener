#!/usr/bin/env python3
"""Script when you just want to run Dellus API."""

import sys
import tempfile

from dellus.core.initialize import initialize, initialize_test


if __name__ == '__main__':

    # TODO: Use argparsep
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        print('Running Dellus API test server')

        config_path = 'dellus/config/dellus_test.cfg'
        db_file_path = tempfile.NamedTemporaryFile(suffix='.db').name
        db_path = "sqlite:///{}".format(db_file_path)

        initialize_test(config_path, db_url=db_path)
    else:
        print('Running Dellus API server')
        initialize()

    from dellus.rest.manage import run
    run()
