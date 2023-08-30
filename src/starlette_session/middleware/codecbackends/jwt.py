import typing

import jwt
from jwt.exceptions import InvalidTokenError
from starlette.datastructures import Secret

from starlette_session.middleware.codecbackends import (
    CodecBackendInterface,
    DecodeError,
)


class JwtCodecBackend(CodecBackendInterface):
    """
    A codec backend for encoding and decoding JWTs.

    Methods
    -------
    decode(value: str)
        Decodes the provided JWT.
    encode(value: dict[str, Any])
        Encodes the provided claims as a JWT.
    """

    def __init__(
        self,
        key: typing.Union[str, Secret],
        algorithm: str,
    ):
        """
        Constructs an instance of a JwtCodecBackend.

        Parameters
        ----------
        key: Union[str, Secret]
            The key used to sign and verify the integrety of the JWT.
        algorithm: str
            The algorithm used to encode and decode the JWT.
        """
        self._key = key
        self._algorithm = algorithm

    def decode(self, value: str) -> typing.Any:
        """
        Verifies the validity, integrity and decodes the provided JWT.

        raises DecodeError if the provided JWT is not valid or has been tampered with.

        Parameters
        ----------
        value: str
            The JWT that is to be decoded

        Returns
        -------
        dict[str, Any]
        """
        try:
            return jwt.decode(value, key=self._key, algorithms=[self._algorithm])
        except InvalidTokenError as ex:
            raise DecodeError("Failed to decode value") from ex

    def encode(self, data: dict[str, typing.Any]) -> str:
        """
        Encodes the provided claims as a JWT.

        Parameters
        ----------
        data: dict[str, Any]
            The claims that are to be encoded as a JWT.

        Returns
        -------
        str
        """
        return str(jwt.encode(data, key=self._key, algorithm=self._algorithm))
