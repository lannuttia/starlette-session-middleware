import typing

from starlette.requests import HTTPConnection

from starlette_session.middleware.authorizationbackends import (
    AuthorizationBackendInterface,
)


class CookieAuthorizationBackend(AuthorizationBackendInterface):
    """
    An authorization backend for retrieving the token through a session cookie.

    Methods
    -------
    get_token(connection: HTTPConnection)
        Retrieves the token from the session cookie.
    """

    def __init__(self, session_cookie: str = "session"):
        """
        Constructs an instance of an CookieAuthorizationBackend.

        Parameters
        ----------
        session_cookie: str
            The name of the session cookie. Defaults to "session".
        """
        self.session_cookie = session_cookie

    def get_token(self, connection: HTTPConnection) -> typing.Union[str, None]:
        """
        Retreives the token from the session cookie.

        Parameters
        ----------
        connection: HTTPConnection
            The connection that the token will be retrieved from.

        Returns
        -------
        Union[str, None]
        """
        if self.session_cookie not in connection.cookies:
            return None
        return str(connection.cookies[self.session_cookie])
