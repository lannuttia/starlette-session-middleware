import abc
import typing

from starlette.requests import HTTPConnection


class AuthorizationBackendInterface(metaclass=abc.ABCMeta):
    """
    An interface that can be used to implement an authorization backend.

    Methods
    -------
    get_token(connection: HTTPConnection)
        gets the token.
    """

    @classmethod
    def __subclasshook__(cls, __subclass: type) -> bool:
        return hasattr(__subclass, "get_token") and callable(__subclass.get_token)

    @abc.abstractmethod
    def get_token(self, connection: HTTPConnection) -> typing.Union[str, None]:
        """
        Raises NotImplementedError

        Parameters
        ----------
        value: HTTPConnection
            The connection that the token can be retrieved from.
        """
        raise NotImplementedError
