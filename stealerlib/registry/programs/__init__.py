#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/registry/programs/__init__.py
"""

from stealerlib.registry import *
from stealerlib.registry.types import RegistryTypes
from stealerlib.registry.manager import RegistryKeyManager


class Programs:
    """This class provides methods for extracting and parsing program-related information from the windows registry using the winreg library

    Attributes:
        programs  A list of program information as a list of values or a StealerLib object for each program stored in the registry
    """

    def __init__(self):
        super(Programs, self).__init__()

        self.programs = []

    @catch
    def get_installed_programs(
        self,
        conv: Optional[bool]=True
    ) -> list[Union[list, list[RegistryTypes.Program]]]:
        """Uses winreg to get all installed programs from the registry, and parses their information

        Parameters:
            self (object): The object passed to the method
            conv (bool): Boolean whether to append the data as a converted value or a StealerLib object

        Returns:
            list: A list of the gathered programs information, stored in another list or a StealerLib object
        """

        with RegistryKeyManager() as reg_key:
            for program in range(winreg.QueryInfoKey(reg_key)[0]):
                subkey_id = winreg.EnumKey(reg_key, program)
                subkey = winreg.OpenKey(reg_key, subkey_id)
                try:
                    obj_program = self.get_program_information(key=subkey)
                    self.programs.append(
                        obj_program.conv() if conv else obj_program
                    )
                except OSError:
                    continue

        return self.programs

    @staticmethod
    def get_program_information(key: winreg.HKEYType) -> RegistryTypes.Program:
        """Uses the provided, and context managed, HKEY to look up and parse the programs information from the registry

        Parameters:
            key (winreg.HKEYType): Windows registry sub-key used to lookup program information
            
        Returns:
            RegistryTypes.Program: A StealerLib object containing the name and folder location of the parsed program
        """

        name = winreg.QueryValueEx(key, "DisplayName")[0]
        location = winreg.QueryValueEx(key, "InstallLocation")[0]
        obj_program = RegistryTypes.Program(name=name, location=location)

        return obj_program


if __name__ == "__main__":
    programs = Programs()
    installed_programs = programs.get_installed_programs()
    for program in installed_programs:
        print(f"Name: {program.name}\nLocation: {program.location}\n")