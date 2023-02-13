#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/browser/types.py
"""


from dataclasses import dataclass


class BrowserTypes:

    @dataclass
    class Login:
        url: str
        username: str
        password: str

        def conv(self) -> list:
            return [self.url, self.username, self.password]
 
    @dataclass
    class Cookie:
        host: str
        name: str
        path: str
        value: str
        expires: bool
        expire_date: str

        def conv(self) -> list:
            return [
                self.host,
                self.expires,
                self.expire_date,
                self.path,
                self.name,
                self.value
            ]
 
    @dataclass
    class Site:
        url: str
        title: str
        timestamp: int

        def conv(self) -> list:
            return [self.url, self.title, self.timestamp]
 
    @dataclass
    class Download:
        tab_url: str
        target_path: str

        def conv(self) -> list:
            return [self.tab_url, self.target_path]
 
    @dataclass
    class Card:
        name: str
        month: str
        year: str
        number: str
        date_modified: str

        def conv(self) -> list:
            return [
                self.name,
                self.month,
                self.year,
                self.number,
                self.date_modified
            ]
