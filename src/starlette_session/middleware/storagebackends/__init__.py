import abc

from starlette.types import Message


class StorageBackendInterface(metaclass=abc.ABCMeta):
    """
    An interface that can be used to implement a storage backend.

    Methods
    -------
    persist(message: Message, data: str)
        Persists the data.
    clear(message: Message)
        Clears the data.
    """

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
        """
        Raises NotImplementedError

        Parameters
        ----------
        message: Message
            The message to persist the data on.
        data: str
            The data to persist.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def clear(self, message: Message) -> None:
        """
        Raises NotImplementedError

        Parameters
        ----------
        message: Message
            The message to clear the data from.
        """
        raise NotImplementedError
