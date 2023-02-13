#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: tests.py
"""

from dataclasses import dataclass


@dataclass
class Process:
    pid: int
    name: str
    status: str
    started: str

    def conv(self):
        return [
            self.pid,
            self.name,
            self.status,
            self.started
        ]


new_process = Process(3294, 'python3', 'running', '09:04:44')
print(new_process.conv())