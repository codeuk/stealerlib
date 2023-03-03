#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/request.py
"""

import requests


class HTTPHandler:
    """This class provides methods for utilizing the requests module to make custom HTTP requests

    Attributes:
        base        Passed URL to use as our API base 
        session     Created requests session used to make HTTP requests
    """

    def __init__(self, base, **kwargs):
        self.base = base
        self.session = requests.Session()

    def request(self, method: str, endpoint:str="/", **kwargs):
        """Requests the given endpoint using the passed method

        Parameters:
            self (object): The object passed to the method
            method (bool): Custom method to use/pass to session.request
            endpoint (str): Endpoint of our API (self.base) to request
            **kwargs (tuple): Other values to pass to session.request

        Returns:
            requests.Request: The result of the custom request method as a Request object
        """

        return self.session.request(method, self.base+endpoint, **kwargs)

    def get(self, endpoint:str="/", **kwargs):
        """Requests the given endpoint using the GET method

        Parameters:
            self (object): The object passed to the method
            endpoint (str): Endpoint of our API (self.base) to request
            **kwargs (tuple): Other values to pass to session.request

        Returns:
            requests.Request: The result of the custom request method as a Request object
        """

        return self.session.get(self.base+endpoint, **kwargs)

    def post(self, endpoint:str="/", **kwargs):
        """Requests the given endpoint using the POST method

        Parameters:
            self (object): The object passed to the method
            endpoint (str): Endpoint of our API (self.base) to request
            **kwargs (tuple): Other values to pass to session.request

        Returns:
            requests.Request: The result of the custom request method as a Request object
        """

        return self.session.post(self.base+endpoint, **kwargs)


if __name__ == '__main__':
    API = HTTPHandler('https://example.com/api')

    API.request(method="post",
                endpoint="/api-endpoint",
                data={"exampleData": 0})

    API.get(endpoint="/api-endpoint",
            headers={"exampleHeader": 1})