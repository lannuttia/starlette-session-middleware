import typing

from starlette.datastructures import MutableHeaders
from starlette.types import Message

from starlette_session.middleware.storagebackends import StorageBackendInterface


class CookieStorageBackend(StorageBackendInterface):
    """
    A backend for Cookie based storage.

    Methods
    -------
    persist(message: Message, data: str)
        Persists the data as a cookie through the "Set-Cookie" HTTP Header.
    clear(message: Message)
        Clears the cookie.
    """

    def __init__(
        self,
        max_age: int = 14 * 24 * 60 * 60,
        session_cookie: str = "session",
        path: str = "/",
        same_site: typing.Literal["lax", "strict", "none"] = "lax",
        https_only: bool = False,
    ):
        """
        Constructs an instance of a CookieStorageBackend.

        Parameters
        ----------
        max_age: int
            The maximum age of the cookie in seconds. Defaults to 1209600.
        session_cookie: str
            The name of the session cookie. Defaults to "session".
        path: str
            The path to restrict the cookie to. Defaults to "/".
        same_site: str
            The same site policy to use for the cookie. Defaults to "lax".
        https_only: bool
            If true, prevents javascript from accessing the cookie through `document.cookie`. Defaults to false.
        """
        self.max_age = max_age
        self.session_cookie = session_cookie
        self.path = path
        self.security_flags = "httponly; samesite=" + same_site
        if https_only:  # Secure flag can be used with HTTPS only
            self.security_flags += "; secure"

    def persist(self, message: Message, data: str) -> None:
        """
        Persists the data provided as a session cookie through the HTTP Set-Cookie header.

        Parameters
        ----------
        message: Message
            The starlette message to be handled.
        data: str
            The data that is to be persisted.

        Returns
        -------
        None
        """
        headers = MutableHeaders(scope=message)
        header_value = (
            "{session_cookie}={data}; path={path}; {max_age}{security_flags}".format(
                session_cookie=self.session_cookie,
                data=data,
                path=self.path,
                max_age=f"Max-Age={self.max_age}; " if self.max_age else "",
                security_flags=self.security_flags,
            )
        )
        headers.append("Set-Cookie", header_value)

    def clear(self, message: Message) -> None:
        """
        Clears the session cookie through the HTTP Set-Cookie header.

        Parameters
        ----------
        message: Message
            The starlette message to be handled.

        Returns
        -------
        None
        """
        headers = MutableHeaders(scope=message)
        header_value = (
            "{session_cookie}={data}; path={path}; {expires}{security_flags}".format(
                session_cookie=self.session_cookie,
                data="null",
                path=self.path,
                expires="expires=Thu, 01 Jan 1970 00:00:00 GMT; ",
                security_flags=self.security_flags,
            )
        )
        headers.append("Set-Cookie", header_value)
