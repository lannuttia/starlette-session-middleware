import abc

from starlette.types import Message


class StorageBackendInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, __subclass: type) -> bool:
        return (
            hasattr(__subclass, "persist")
            and callable(__subclass.persist)
            and hasattr(__subclass, "clear")
            and callable(__subclass.clear)
            or NotImplemented
        )

    @abc.abstractmethod
    def persist(self, message: Message, data: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def clear(self, message: Message) -> None:
        raise NotImplementedError
