#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/system/__init__.py
"""

import os
import psutil
import platform

from typing import Union

from stealerlib.exceptions import catch
from stealerlib.datatypes import SystemTypes

from stealerlib.system.processes import Processes


class System(Processes):
    """This class provides methods for extracting and interacting with system related information
        - for multiple different operating systems by utilizing the psutil package
    
    Supported Platforms (from psutil PyPI page):
        Linux
        Windows
        macOS
        FreeBSD, OpenBSD, NetBSD
        Sun Solaris
        AIX
    """

    def __init__(self):
        Processes.__init__(self)

        self.platform = platform.system()