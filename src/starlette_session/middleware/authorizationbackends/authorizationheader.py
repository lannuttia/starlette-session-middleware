import re
import typing

from starlette.requests import HTTPConnection

from starlette_session.middleware.authorizationbackends import (
    AuthorizationBackendInterface,
)


class AuthorizationHeaderAuthorizationBackend(AuthorizationBackendInterface):
    """
    An authorization backend for retrieving the token through the HTTP Authorization header.

    Methods
    -------
    get_token(connection: HTTPConnection)
        Retrieves the token from the HTTP Authorization header.
    """

    def __init__(self, type: str = "Bearer"):
        """
        Constructs an instance of an AuthorizationHeaderAuthorizationBackend.

        Parameters
        ----------
        type: str
            The token type that is expected.
        """
        self.pattern = re.compile(f"^{type.lower()} (.*)$", re.I)

    def get_token(self, connection: HTTPConnection) -> typing.Union[str, None]:
        """
        Retreives the token from the HTTP Authorization header.

        Parameters
        ----------
        connection: HTTPConnection
            The connection that the token will be retrieved from.

        Returns
        -------
        Union[str, None]
        """
        header = "Authorization"
        if header not in connection.headers:
            return None
        value = connection.headers[header]
        match = self.pattern.match(value)
        return str(match[1]) if match is not None else None
