#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/system/decorators.py
"""

import platform

from stealerlib.exceptions import *

# currently unused, will be implemented into stealerlib.system when there's a solid *nix stealer base

def windows(func: callable) -> callable:
    """A function decorator that catches any calls for functions only-for the wrong operating system

    Parameters:
        func (function): The function to decorate and handle

    Returns:
        function: The decorated function

    Example:
        @windows
        def handled_function():
            # Function code here
    """

    def checker(*args, **kwargs):
        if platform.system() == "Windows":
            func(*args, **kwargs)
        else:
            raise InvalidOperatingSystemCall("{} is a Windows-only function".format(func.__name__))

    return checker

def linux(func: callable) -> callable:
    """A function decorator that catches any calls for functions only-for the wrong operating system

    Parameters:
        func (function): The function to decorate and handle

    Returns:
        function: The decorated function

    Example:
        @linux
        def handled_function():
            # Function code here
    """

    def checker(*args, **kwargs):
        if platform.system() == "Linux":
            func(*args, **kwargs)
        else:
            raise InvalidOperatingSystemCall("{} is a Linux-only function".format(func.__name__))

    return checker