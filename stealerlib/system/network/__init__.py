#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/system/network/__init__.py
"""

from stealerlib.system import *
from stealerlib.system.network.wifi import WiFi
from stealerlib.system.types import SystemTypes


class Network(WiFi):
    """This class provides methods for extracting network-related information using subprocess and windows commands"""

    def __init__(self):
        super(Network, self).__init__()

        self.addresses = []
        self.interfaces = []

    def get_network_interfaces(
        self,
        conv: Optional[bool]=True
    ) -> list[Union[list, SystemTypes.NetworkInterface]]:
        """A function decorator that catches and handles any exceptions thrown

        Parameters:
            self (object): The object passed to the method
            conv (bool): Boolean whether to append the data as a converted list of values or a StealerLib object

        Returns:
            list: A list of the gathered network interfaces information, appended as a list or StealerLib objects
        """

        for iface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == 2:
                    self.addresses.append(addr.address)

            obj_interface = SystemTypes.NetworkInterface(iface, self.addresses)
            self.interfaces.append(
                obj_interface.conv() if conv else obj_interface
            )

        return self.interfaces