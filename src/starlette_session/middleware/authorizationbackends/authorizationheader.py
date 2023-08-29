import typing


from starlette.requests import HTTPConnection


from starlette_session.middleware.authorizationbackends import (
    AuthorizationBackendInterface,
)


class AuthorizationHeaderAuthorizationBackend(AuthorizationBackendInterface):
    def __init__(self, type: str = "Bearer"):
        self.type = type

    def get_token(self, connection: HTTPConnection) -> typing.Union[str, None]:
        header = "Authorization"
        expected_value_prefix = f"{self.type} "
        if header not in connection.headers or not connection.headers[
            header
        ].startswith(expected_value_prefix):
            return None
        return str(connection.headers[header].split(expected_value_prefix, 1)[1])
