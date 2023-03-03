#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/system/__init__.py
"""

import os
import wmi
import math
import psutil
import platform
import requests

from typing import Union, Optional

from stealerlib.exceptions import catch

from stealerlib.system.cpu import CPU
from stealerlib.system.mem import Memory
from stealerlib.system.types import SystemTypes


class System(CPU, Memory):
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

        self.platform = platform.system()
        self.__load__()

    @catch
    @staticmethod
    def get_ip() -> str:
        ip = requests.get("https://icanhazip.com/").text

        return ip.splitlines()[0]

    @staticmethod
    def convert_bytes(size: bytes) -> str:
        if not size:
            return "0B"

        sizes = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size, 1024)))
        pow = math.pow(1024, i)
        size = round(size / pow, 2)

        return "%s %s" % (size, sizes[i])

    def __load__(self):
        system = wmi.WMI()
        self.comp_info = system.Win32_ComputerSystem()[0]
        self.os_info = osi = system.Win32_OperatingSystem()[0]
        self.proc_info = system.Win32_Processor()[0]
        self.gpu_info = system.Win32_VideoController()[0]

        self.os_name = osi.Name.encode('utf-8').split(b'|')[0]
        self.os_build = osi.BuildNumber
        self.os_version = osi.Version
        self.ram = self.convert_bytes(float(osi.TotalVisibleMemorySize))
