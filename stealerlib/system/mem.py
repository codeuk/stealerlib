#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/system/mem.py
"""

from stealerlib.system import *
from stealerlib.system.types import SystemTypes

swap_memory = psutil.swap_memory
get_virtual_mem = psutil.virtual_memory


class Memory:
    """This class provides methods for extracting and parsing memory-related information using the psutil library

    Attributes:
        partitions  A list of partition information as a list of values or a StealerLib object for each available device partition
    """

    def __init__(self):
        super(Memory, self).__init__()

        self.partitions = []

    @catch
    def get_partitions(
        self,
        conv: Optional[bool]=True
    ) -> list[Union[list, SystemTypes.Partition]]:
        """Uses psutil to get all disk partitions, and parses their information

        Parameters:
            self (object): The object passed to the method
            conv (bool): Boolean whether to append the data as a converted list of values or a StealerLib object

        Returns:
            list: A list of the gathered processes information, appended as a list or StealerLib objects
        """

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