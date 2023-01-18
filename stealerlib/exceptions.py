#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/exceptions.py
"""

debug = False

def quiet(func):
    def handle(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as error:
            if debug:
                print("[!] StealerLib handled an unexpected error: {}".format(error))
            pass
    return handle