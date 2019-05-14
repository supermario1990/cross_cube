#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import L, get_logger
from server import create_app
import os
from db import *

print(L("Hello world!"))
app = create_app(os.getenv('KROS_CONFIG') or 'default')
print(app.url_map)
app.run()
