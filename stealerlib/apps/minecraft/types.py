#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/apps/minecraft/types.py
"""

from dataclasses import dataclass


class MinecraftTypes:

    @dataclass
    class Account:
        email: str
        username: str
        uuid: str
        token: str

        def conv(self) -> list:
            return [
                self.email,
                self.username,
                self.uuid,
                self.token
            ]
