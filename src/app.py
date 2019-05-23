#!/usr/bin/env python
# -*- coding: utf-8 -*-

from server import create_app
from db import db_base
import os

app = create_app(os.getenv('KROS_CONFIG') or 'default')
app.run()
