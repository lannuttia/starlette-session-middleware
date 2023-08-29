import json
import typing
from base64 import b64decode, b64encode

import itsdangerous
from itsdangerous.exc import BadSignature

from starlette.datastructures import Secret

from starlette_session.middleware.codecbackends.errors import DecodeError
from starlette_session.middleware.codecbackends import CodecBackendInterface


class SignerBackend(CodecBackendInterface):
    def __init__(
        self,
        key: typing.Union[str, Secret],
        max_age: typing.Optional[int] = 14 * 24 * 60 * 60,
    ):
        self.signer = itsdangerous.TimestampSigner(str(key))
        self.max_age = max_age

    def decode(self, value: str) -> typing.Any:
        try:
            data = self.signer.unsign(value, max_age=self.max_age)
            return json.loads(b64decode(data))
        except BadSignature as ex:
            raise DecodeError("Failed to decode value") from ex

    def encode(self, data: dict[str, typing.Any]) -> str:
        base64_encoded_data = b64encode(json.dumps(data).encode("utf-8"))
        return str(self.signer.sign(base64_encoded_data).decode("utf-8"))
