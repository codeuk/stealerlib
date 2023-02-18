#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/system/mem.py
"""

from stealerlib.system import *
from stealerlib.system.types import SystemTypes


class Memory:
    def __init__(self):
        self.partitions = []

    @catch
    def get_partitions(self, conv: Optional[bool]=True) -> list:
        partitions = psutil.disk_partitions()

        for p in partitions:
            obj_partition = SystemTypes.Partition(
                p.device,
                p.mountpoint,
                p.fstype,
                p.maxpath,
                p.maxfile
            )
            self.partitions.append(
                obj_partition.conv() if conv else obj_partition
            )

        return self.partitions

    @catch
    def get_virtual_mem(self):

        return psutil.virtual_memory()

    @catch
    def swap_memory(self):

        return psutil.swap_memory()