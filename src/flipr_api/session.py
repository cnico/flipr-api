# -*- coding: utf-8 -*-
"""Session manager for the Flipr REST API in order to maintain authentication token between calls."""
from requests import Response
from requests import Session

from .const import FLIPR_API_URL
from .const import FLIPR_AUTH_URL


class FliprClientSession(Session):
    """HTTP session manager for Flipr api.

    This session object allows to manage the authentication
    in the API using a token.
    """

    host: str = FLIPR_API_URL

    def __init__(self, username: str, password: str) -> None:
        """Initialize and authenticate.

        Args:
            username: the flipr registered user
            password: the flipr user's password
        """
        Session.__init__(self)

        # Authenticate with user and pass and store bearer token
        payload_token = (
            "grant_type=password&username=" + username + "&password=" + password
        )
        headers_token = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        }
        response = super().request(
            "POST", FLIPR_AUTH_URL, data=payload_token, headers=headers_token
        )
        response.raise_for_status()
        # print(response.text)

        self.bearerToken = str(response.json()["access_token"])
        # print("BearerToken of authentication : " + self.bearerToken)

    def rest_request(self, method: str, path: str) -> Response:
        """Make a request using token authentication.

        Args:
            method: Method for the HTTP request (example "GET" or "POST").
            path: path of the REST API endpoint.

        Returns:
            the Response object corresponding to the result of the API request.
        """
        headers_auth = {
            "Authorization": "Bearer " + self.bearerToken,
            "Cache-Control": "no-cache",
        }

        response = super().request(method, f"{self.host}/{path}", headers=headers_auth)
        response.raise_for_status()

        return response
