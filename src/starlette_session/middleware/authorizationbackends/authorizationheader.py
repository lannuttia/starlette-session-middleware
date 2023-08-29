import re
import typing


from starlette.requests import HTTPConnection


from starlette_session.middleware.authorizationbackends import (
    AuthorizationBackendInterface,
)


class AuthorizationHeaderAuthorizationBackend(AuthorizationBackendInterface):
    def __init__(self, type: str = "Bearer"):
        self.pattern = re.compile(f"^{type.lower()} (.*)$", re.I)

    def get_token(self, connection: HTTPConnection) -> typing.Union[str, None]:
        header = "Authorization"
        if header not in connection.headers:
            return None
        value = connection.headers[header]
        match = self.pattern.match(value)
        return str(match[1]) if match is not None else None
