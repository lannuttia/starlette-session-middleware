import typing

import jwt
from jwt.exceptions import InvalidTokenError

from starlette.datastructures import Secret

from starlette_session.middleware.codecbackends.errors import DecodeError
from starlette_session.middleware.codecbackends import CodecBackendInterface


class JwtBackend(CodecBackendInterface):
    def __init__(
        self,
        key: typing.Union[str, Secret],
        algorithm: str,
    ):
        self.key = key
        self.algorithm = algorithm

    def decode(self, value: str) -> typing.Any:
        try:
            return jwt.decode(value, key=self.key, algorithms=[self.algorithm])
        except InvalidTokenError as ex:
            raise DecodeError("Failed to decode value") from ex

    def encode(self, data: dict[str, typing.Any]) -> str:
        return str(jwt.encode(data, key=self.key, algorithm=self.algorithm))
