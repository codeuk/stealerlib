#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/datatypes.py
"""


class DataTypes:

    class Login:
        def __init__(self, url, username, password):
            self.url = url
            self.username = username
            self.password = password

        def conv(self) -> list:
            return [self.url, self.username, self.password]

    class Cookie:
        def __init__(self, host, name, path, value, expires):
            self.host = host
            self.name = name
            self.path = path
            self.value = value
            self.expires = bool(expires)
            self.expire_date = expires

        def conv(self) -> list:
            return [
                self.host,
                self.expires,
                self.expire_date,
                self.path,
                self.name,
                self.value
            ]

    class Site:
        def __init__(self, url, title, timestamp):
            self.url = url
            self.title = title
            self.timestamp = timestamp

        def conv(self) -> list:
            return [self.url, self.title, self.timestamp]

    class Download:
        def __init__(self, tab_url, target_path):
            self.tab_url = tab_url
            self.target_path = target_path

        def conv(self) -> list:
            return [self.tab_url, self.target_path]

    class Card:
        def __init__(self, name, month, year, number, date_modified):
            self.name = name
            self.month = month
            self.year = year
            self.number = number
            self.date_modified = date_modified

        def conv(self) -> list:
            return [
                self.name,
                self.month,
                self.year,
                self.number,
                self.date_modified
            ]
