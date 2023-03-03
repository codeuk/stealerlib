#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/registry/manager.py
"""

import winreg

WIN_REG_PROGRAM_PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
WIN_REG_HKEY = winreg.OpenKey(
    winreg.HKEY_LOCAL_MACHINE,
    WIN_REG_PROGRAM_PATH
)


class RegistryKeyManager:
    def __enter__(self):
        return WIN_REG_HKEY

    def __exit__(self, exc_type, exc_value, exc_tb):
        WIN_REG_HKEY.Close()


if __name__ == '__main__':
    with RegistryKeyManager() as reg_key:
        for program in range(winreg.QueryInfoKey(reg_key)[0]):
            subkey_id = winreg.EnumKey(reg_key, program)
            subkey = winreg.OpenKey(reg_key, subkey_id)
            print(reg_key, subkey, subkey_id)