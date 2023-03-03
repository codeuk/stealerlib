#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/system/cpu/processes.py
"""

from stealerlib.system import *
from stealerlib.system.types import SystemTypes


class Processes:
    """This class provides methods for extracting and parsing process-related information using the psutil library

    Attributes:
        processes  A list of device process information as a list of values or a StealerLib object for each available process
    """

    def __init__(self):
        super(Processes, self).__init__()

        self.processes = []

    @catch
    def get_processes(
        self,
        conv: Optional[bool]=True
    ) -> list[Union[list, SystemTypes.Process]]:
        """Uses psutil to get all process id's, and uses get_process to get each processes information

        Parameters:
            self (object): The object passed to the method
            conv (bool): Boolean whether to append the data as a converted value or a StealerLib object

        Returns:
            list: A list of the scraped processes appended as a list or StealerLib objects
        """

        pids = psutil.pids()

        for pid in pids:
            obj_process = self.get_process(pid=pid)
            if obj_process:
                self.processes.append(
                    obj_process.conv() if conv else obj_process
                )

        return self.processes

    def get_process(self, pid: int) -> SystemTypes.Process:
        """Uses psutil to get information on a process using its supplied process id

        Parameters:
            self (object): The object passed to the method
            pid (int): The processes id to look up

        Returns:
            SystemTypes.Process: A StealerLib object containing information on the process and interactivity
        """

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
        """Kills a process using psutil with the supplied process id"""

        p = psutil.Process(pid)
        p.kill()

    @catch
    def terminate_process(self, pid: int) -> None:
        """Terminates a process using psutil with the supplied process id"""

        p = psutil.Process(pid)
        p.terminate()
