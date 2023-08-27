import abc
import typing


class CodecBackendInterface(metaclass=abc.ABCMeta):
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
        raise NotImplementedError

    @abc.abstractmethod
    def encode(self, value: dict[str, typing.Any]) -> str:
        raise NotImplementedError
