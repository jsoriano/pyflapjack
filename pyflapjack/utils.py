#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json


class FlapjackError(Exception):
    pass
