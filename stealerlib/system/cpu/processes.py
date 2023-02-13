#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/system/processes.py
"""

from stealerlib.system import *
from stealerlib.system.types import SystemTypes


class Processes:
    def __init__(self):
        self.processes = []

    @catch
    def get_processes(self, conv: bool=True) -> list:
        pids = psutil.pids()

        for pid in pids:
            obj_process = self.get_process(pid=pid)
            if obj_process:
                self.processes.append(
                    obj_process.conv() if conv else obj_process
                )

        return self.processes

    def get_process(self, pid: int) -> Union[None, SystemTypes.Process]:
        p = psutil.Process(pid)

        process = SystemTypes.Process(
            pid=pid,
            name=p.name(),
            status=p.status(),
            parent=p.parent(),
            children=p.children()
        )

        return process

    @catch
    def kill_process(self, pid: int) -> None:
        p = psutil.Process(pid)
        p.kill()

    @catch
    def terminate_process(self, pid: int) -> None:
        p = psutil.Process(pid)
        p.terminate()
