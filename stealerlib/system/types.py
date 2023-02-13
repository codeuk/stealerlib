#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/system/types.py
"""

import psutil

from dataclasses import dataclass

from stealerlib.exceptions import catch


class SystemTypes:

    @dataclass
    class Process:
        pid: int
        name: str
        status: str
        parent: list[psutil.Process]
        children: list[psutil.Process]

        def conv(self) -> list:
            return [
                self.pid,
                self.name,
                self.status,
                self.parent,
                self.children
            ]

        @catch
        def kill(self):
            p = psutil.Process(self.pid)
            p.kill()

        @catch
        def terminate(self):
            p = psutil.Process(self.pid)
            p.terminate()

    @dataclass
    class Partition:
        device: str
        mountpoint: str
        filesystem: str
        maxpaths: int
        maxfiles: int

        def conv(self) -> list:
            return [
                self.device,
                self.mountpoint,
                self.filesystem,
                self.maxpaths,
                self.maxfiles
            ]

        def usage(self):
            disk_usage = psutil.disk_usage(self.device)

            return disk_usage
