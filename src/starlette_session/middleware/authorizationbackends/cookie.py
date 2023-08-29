import typing


from starlette.requests import HTTPConnection


from starlette_session.middleware.authorizationbackends import (
    AuthorizationBackendInterface,
)


class CookieAuthorizationBackend(AuthorizationBackendInterface):
    def __init__(self, session_cookie: str = "session"):
        self.session_cookie = session_cookie

    def get_token(self, connection: HTTPConnection) -> typing.Union[str, None]:
        if self.session_cookie not in connection.cookies:
            return None
        return str(connection.cookies[self.session_cookie])
