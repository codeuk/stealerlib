#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/system/__init__.py
"""

from stealerlib.exceptions import catch


class System:
    def __init__(self):
        pass

    @catch
    def get_ip(self) -> str:
        return ""