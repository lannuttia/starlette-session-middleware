import abc
import typing


class CodecBackendInterface(metaclass=abc.ABCMeta):
    """
    An interface that can be used to implement a codec backend.

    Methods
    -------
    decode(value: str)
        Decodes the provided string.
    encode(value: dict[str, Any])
        Encodes the provided dictionary.
    """

    @classmethod
    def __subclasshook__(cls, __subclass: type) -> bool:
        return (
            hasattr(__subclass, "decode")
            and callable(__subclass.decode)
            and hasattr(__subclass, "encode")
            and callable(__subclass.encode)
            or NotImplemented
        )

    @abc.abstractmethod
    def decode(self, value: str) -> typing.Any:
        """
        Raises NotImplementedError

        Parameters
        ----------
        value: str
            The string to be decoded.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def encode(self, value: dict[str, typing.Any]) -> str:
        """
        Raises NotImplementedError

        Parameters
        ----------
        value: dict[str, Any]
            The value to be encoded.
        """
        raise NotImplementedError


class DecodeError(Exception):
    """
    An error to raise if decoding a token can not or should not happen.
    """

    pass
