#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import decimal
import json
import datetime
from sqlalchemy.ext.declarative import DeclarativeMeta


class JSONEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        """
        创建JSON编码器，用于转换某些类型的数据。
        """
        super(JSONEncoder, self).__init__(*args, **kwargs)
        self.iterator_limit = 1000

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return json.JSONEncoder.default(self, obj)

        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        if hasattr(obj, "to_dict") and callable(getattr(obj, "to_dict")):
            return obj.to_dict()
        else:
            array = None
            try:
                iterator = iter(obj)
                count = self.iterator_limit
                array = []
                for i, obj in enumerate(iterator):
                    array.append(obj)
                    if i >= count:
                        break
            except TypeError as e:
                pass

            if array is not None:
                return array
            else:
                return json.JSONEncoder.default(self, obj)
