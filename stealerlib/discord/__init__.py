#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/discord/__init__.py
"""

from stealerlib.exceptions import catch


class Discord:

    def __init__(self):
        self.tokens = []
        self.accounts = []

    @catch
    def get_tokens(self) -> list:
        return []