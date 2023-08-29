import pytest


from starlette.types import Scope
from starlette.requests import HTTPConnection


from starlette_session.middleware.authorizationbackends.cookie import (
    CookieAuthorizationBackend,
)
from starlette_session.middleware.authorizationbackends import (
    AuthorizationBackendInterface,
)


class TestCookieAuthorizationBackend:
    def test_is_expected_subclass(self):
        cookie_authorization_backend = CookieAuthorizationBackend()
        assert isinstance(cookie_authorization_backend, AuthorizationBackendInterface)

    session_cookies = [
        "session",
        "garbage",
        "test",
    ]

    @pytest.mark.parametrize("session_cookie", session_cookies)
    def test_session_cookie(self, session_cookie):
        cookie_authorization_backend = CookieAuthorizationBackend(
            session_cookie=session_cookie
        )
        token = "somegarbagetoken"
        cookie = f"{session_cookie}={token}; path=/; httponly; samesite=lax"
        scope = {
            "type": "http",
            "headers": [["cookie".encode("latin-1"), cookie.encode("latin-1")]],
        }
        connection = HTTPConnection(scope=scope)
        assert cookie_authorization_backend.get_token(connection) == token

    @pytest.mark.parametrize("session_cookie", session_cookies)
    def test_no_session_cookie(self, session_cookie):
        cookie_authorization_backend = CookieAuthorizationBackend(
            session_cookie=session_cookie
        )
        cookie = ""
        scope = {
            "type": "http",
            "headers": [["cookie".encode("latin-1"), cookie.encode("latin-1")]],
        }
        connection = HTTPConnection(scope=scope)
        assert cookie_authorization_backend.get_token(connection) is None
