#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/registry/__init__.py
"""

import winreg

from typing import Union, Optional

from stealerlib.exceptions import catch

from stealerlib.registry.programs import Programs
from stealerlib.registry.types import RegistryTypes
from stealerlib.registry.manager import RegistryKeyManager


class Registry(Programs):
    """This class provides methods for extracting and parsing information from the windows registry using the winreg library"""

    def __init__(self):
        super(Registry, self).__init__()
