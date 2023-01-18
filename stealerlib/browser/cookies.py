#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/browser/cookies.py
"""

from stealerlib.browser import *
from stealerlib.exceptions import quiet


class CookieStealer:

    def __init__(self):
        self.cookies = []

    @quiet
    def get_cookies(self) -> list[tuple[str, ...]]:
        """Unfinished"""
        return [("")]