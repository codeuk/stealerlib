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

from stealerlib.system.cpu import CPU
from stealerlib.system.mem import Memory
from stealerlib.system.types import SystemTypes


class System(CPU, Memory):
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
        CPU.__init__(self)
        Memory.__init__(self)

        self.platform = platform.system()