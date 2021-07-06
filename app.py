#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app

app = create_app(os.getenv('FLASK_ENV') or 'default')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
