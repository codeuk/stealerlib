#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/request.py
"""

import requests


class HTTPHandler:
    def __init__(self, base, **kwargs):
        self.base = base
        self.session = requests.Session()

        for arg in kwargs:
            if isinstance(kwargs[arg], dict):
                kwargs[arg] = self._merge(getattr(self.session, arg), kwargs[arg])
            setattr(self.session, arg, kwargs[arg])

    def request(self, method, endpoint, **kwargs):
        return self.session.request(method, self.base+endpoint, **kwargs)

    def get(self, endpoint, **kwargs):
        return self.session.get(self.base+endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.session.post(self.base+endpoint, **kwargs)

    @staticmethod
    def _merge(source, destination):
        for key, value in source.items():
            if isinstance(value, dict):
                node = destination.setdefault(key, {})
                HTTPHandler._merge(value, node)
            else:
                destination[key] = value
        return destination
