#!/usr/bin/env python3
from dellus.core.initialize import initialize
initialize()
from dellus.rest.manage import app

if __name__ == '__main__':
    app.run()
