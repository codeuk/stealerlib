#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/registry/programs/types.py
"""

from dataclasses import dataclass


class RegistryTypes:

    @dataclass
    class Program:
        name: str
        location: str

        def conv(self) -> list:
            return [self.name, self.location]