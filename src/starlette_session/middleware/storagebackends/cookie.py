import typing


from starlette.datastructures import MutableHeaders
from starlette.types import Message

from starlette_session.middleware.storagebackends import StorageBackendInterface


class CookieBackend(StorageBackendInterface):
    def __init__(
        self,
        max_age: typing.Optional[int] = 14 * 24 * 60 * 60,
        session_cookie: str = "session",
        path: str = "/",
        same_site: typing.Literal["lax", "strict", "none"] = "lax",
        https_only: bool = False,
    ):
        self.max_age = max_age
        self.session_cookie = session_cookie
        self.path = path
        self.security_flags = "httponly; samesite=" + same_site
        if https_only:  # Secure flag can be used with HTTPS only
            self.security_flags += "; secure"

    def persist(self, message: Message, data: str) -> None:
        headers = MutableHeaders(scope=message)
        header_value = "{session_cookie}={data}; path={path}; {max_age}{security_flags}".format(  # noqa E501
            session_cookie=self.session_cookie,
            data=data,
            path=self.path,
            max_age=f"Max-Age={self.max_age}; " if self.max_age else "",
            security_flags=self.security_flags,
        )
        headers.append("Set-Cookie", header_value)

    def clear(self, message: Message) -> None:
        headers = MutableHeaders(scope=message)
        header_value = "{session_cookie}={data}; path={path}; {expires}{security_flags}".format(  # noqa E501
            session_cookie=self.session_cookie,
            data="null",
            path=self.path,
            expires="expires=Thu, 01 Jan 1970 00:00:00 GMT; ",
            security_flags=self.security_flags,
        )
        headers.append("Set-Cookie", header_value)
