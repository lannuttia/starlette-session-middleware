import abc
import typing


from starlette.requests import HTTPConnection


class AuthorizationBackendInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, __subclass: type) -> bool:
        return hasattr(__subclass, "get_token") and callable(__subclass.get_token)

    @abc.abstractmethod
    def get_token(self, connection: HTTPConnection) -> typing.Union[str, None]:
        raise NotImplementedError
