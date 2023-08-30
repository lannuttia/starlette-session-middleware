import json
import typing
from base64 import b64decode, b64encode

import itsdangerous
from itsdangerous.exc import BadSignature
from starlette.datastructures import Secret

from starlette_session.middleware.codecbackends import (
    CodecBackendInterface,
    DecodeError,
)


class SignerCodecBackend(CodecBackendInterface):
    """
    A codec backend for encoding and decoding signed tokens.

    Methods
    -------
    decode(value: str)
        Decodes the provided token.
    encode(value: dict[str, Any])
        Encodes the provided dict as a signed token.
    """

    def __init__(
        self,
        key: typing.Union[str, Secret],
        max_age: typing.Optional[int] = 14 * 24 * 60 * 60,
    ):
        """
        Constructs an instance of a SignerCodecBackend.

        Parameters
        ----------
        key: Union[str, Secret]
            The key used to sign and verify the integrety of the token.
        max_age: Optional[int]
            The maximum allowable age of the token. Defaults to 1,209,600 seconds (14 days).
        """
        self.signer = itsdangerous.TimestampSigner(str(key))
        self.max_age = max_age

    def decode(self, value: str) -> typing.Any:
        """
        Verifies the validity and decodes the provided token.

        raises DecodeError if the provided token is not valid.

        Parameters
        ----------
        value: str
            The token that is to be decoded

        Returns
        -------
        dict[str, Any]
        """
        try:
            data = self.signer.unsign(value, max_age=self.max_age)
            return json.loads(b64decode(data))
        except BadSignature as ex:
            raise DecodeError("Failed to decode value") from ex

    def encode(self, data: dict[str, typing.Any]) -> str:
        """
        Encodes the provided data as a token.

        Parameters
        ----------
        data: dict[str, Any]
            The data that is to be encoded as a token.

        Returns
        -------
        str
        """
        base64_encoded_data = b64encode(json.dumps(data).encode("utf-8"))
        return str(self.signer.sign(base64_encoded_data).decode("utf-8"))
