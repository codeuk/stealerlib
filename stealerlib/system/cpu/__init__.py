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

        self.platform = self.get_processor_name()

    @catch
    def get_processor_name(self):
        if platform.system() == "Windows":
            return platform.processor()
        elif platform.system() == "Darwin":
            os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
            command ="sysctl -n machdep.cpu.brand_string"
            return subprocess.check_output(command).strip()
        elif platform.system() == "Linux":
            command = "cat /proc/cpuinfo"
            all_info = subprocess.check_output(command, shell=True).decode().strip()
            for line in all_info.split("\n"):
                if "model name" in line:
                    return re.sub( ".*model name.*:", "", line,1)
        return ""