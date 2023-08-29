import pytest
from starlette.requests import HTTPConnection

from starlette_session.middleware.authorizationbackends import (
    AuthorizationBackendInterface,
)


class TestAuthorizationBackendInterface:
    def test_isinstance_behavior(self):
        class DummyAuthorizationBackend(AuthorizationBackendInterface):
            def get_token(self, _: HTTPConnection) -> str:
                return ""

        assert (
            isinstance(DummyAuthorizationBackend(), AuthorizationBackendInterface)
            is True
        )

    def test_instantiation(self):
        with pytest.raises(TypeError):
            AuthorizationBackendInterface()  # type: ignore

    def test_get_token(self):
        class DummyAuthorizationBackend(AuthorizationBackendInterface):
            def get_token(self, connection: HTTPConnection) -> str:
                return super().get_token(connection)  # type: ignore

        backend = DummyAuthorizationBackend()
        scope = {
            "type": "http",
        }
        connection = HTTPConnection(scope)
        with pytest.raises(NotImplementedError):
            backend.get_token(connection)
