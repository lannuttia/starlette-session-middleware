import typing

import pytest

from starlette_session.middleware.storagebackends import StorageBackendInterface
from starlette.requests import cookie_parser
from starlette_session.middleware.storagebackends.cookie import CookieStorageBackend


class CookieBackendKwargs(typing.TypedDict):
    max_age: typing.Optional[int]
    session_cookie: str
    path: str
    same_site: typing.Literal["lax", "strict", "none"]
    https_only: bool


class TestCookieStorageBackend:
    def test_expected_subclass(self):
        cookie_backend = CookieStorageBackend()
        assert isinstance(cookie_backend, StorageBackendInterface) is True

    def test_default_persist(self):
        cookie_backend = CookieStorageBackend()
        value = "somegarbage"
        scope = {"type": "http", "headers": []}
        cookie_backend.persist(scope, value)
        assert scope["type"] == "http"
        assert len(scope["headers"]) == 1
        assert isinstance(scope["headers"][0], tuple)
        assert scope["headers"][0][0] == "set-cookie".encode("latin-1")
        assert cookie_parser(scope["headers"][0][1].decode("latin-1")) == cookie_parser(
            "session=somegarbage; path=/; Max-Age=1209600; httponly; samesite=lax"
        )

    def test_default_clear(self):
        cookie_backend = CookieStorageBackend()
        scope = {"type": "http", "headers": []}
        cookie_backend.clear(scope)
        assert scope["type"] == "http"
        assert len(scope["headers"]) == 1
        assert isinstance(scope["headers"][0], tuple)
        assert scope["headers"][0][0] == "set-cookie".encode("latin-1")
        assert cookie_parser(scope["headers"][0][1].decode("latin-1")) == cookie_parser(
            "session=null; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT; httponly; samesite=lax"
        )

    cookie_backend_kwargs: list[CookieBackendKwargs] = [
        CookieBackendKwargs(
            max_age=0,
            session_cookie="cookie_name",
            path="/another/path",
            same_site="strict",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=0,
            session_cookie="cookie_name",
            path="/another/path",
            same_site="lax",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=0,
            session_cookie="cookie_name",
            path="/another/path",
            same_site="none",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=0,
            session_cookie="cookie_name",
            path="/another/path",
            same_site="strict",
            https_only=False,
        ),
        CookieBackendKwargs(
            max_age=0,
            session_cookie="cookie_name",
            path="/another/path",
            same_site="lax",
            https_only=False,
        ),
        CookieBackendKwargs(
            max_age=0,
            session_cookie="cookie_name",
            path="/another/path",
            same_site="none",
            https_only=False,
        ),
        CookieBackendKwargs(
            max_age=0,
            session_cookie="cookie_name",
            path="/yet/another/path",
            same_site="strict",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=0,
            session_cookie="cookie_name",
            path="/yet/another/path",
            same_site="lax",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=0,
            session_cookie="cookie_name",
            path="/yet/another/path",
            same_site="none",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=0,
            session_cookie="cookie_name",
            path="/yet/another/path",
            same_site="strict",
            https_only=False,
        ),
        CookieBackendKwargs(
            max_age=0,
            session_cookie="cookie_name",
            path="/yet/another/path",
            same_site="lax",
            https_only=False,
        ),
        CookieBackendKwargs(
            max_age=0,
            session_cookie="cookie_name",
            path="/yet/another/path",
            same_site="none",
            https_only=False,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="cookie_name",
            path="/another/path",
            same_site="strict",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="cookie_name",
            path="/another/path",
            same_site="lax",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="cookie_name",
            path="/another/path",
            same_site="none",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="cookie_name",
            path="/another/path",
            same_site="strict",
            https_only=False,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="cookie_name",
            path="/another/path",
            same_site="lax",
            https_only=False,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="cookie_name",
            path="/another/path",
            same_site="none",
            https_only=False,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="cookie_name",
            path="/yet/another/path",
            same_site="strict",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="cookie_name",
            path="/yet/another/path",
            same_site="lax",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="cookie_name",
            path="/yet/another/path",
            same_site="none",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="cookie_name",
            path="/yet/another/path",
            same_site="strict",
            https_only=False,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="cookie_name",
            path="/yet/another/path",
            same_site="lax",
            https_only=False,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="cookie_name",
            path="/yet/another/path",
            same_site="none",
            https_only=False,
        ),
        CookieBackendKwargs(
            max_age=0,
            session_cookie="yet_another_cookie_name",
            path="/another/path",
            same_site="strict",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=0,
            session_cookie="yet_another_cookie_name",
            path="/another/path",
            same_site="lax",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=0,
            session_cookie="yet_another_cookie_name",
            path="/another/path",
            same_site="none",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=0,
            session_cookie="yet_another_cookie_name",
            path="/another/path",
            same_site="strict",
            https_only=False,
        ),
        CookieBackendKwargs(
            max_age=0,
            session_cookie="yet_another_cookie_name",
            path="/another/path",
            same_site="lax",
            https_only=False,
        ),
        CookieBackendKwargs(
            max_age=0,
            session_cookie="yet_another_cookie_name",
            path="/another/path",
            same_site="none",
            https_only=False,
        ),
        CookieBackendKwargs(
            max_age=0,
            session_cookie="yet_another_cookie_name",
            path="/yet/another/path",
            same_site="strict",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=0,
            session_cookie="yet_another_cookie_name",
            path="/yet/another/path",
            same_site="lax",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=0,
            session_cookie="yet_another_cookie_name",
            path="/yet/another/path",
            same_site="none",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=0,
            session_cookie="yet_another_cookie_name",
            path="/yet/another/path",
            same_site="strict",
            https_only=False,
        ),
        CookieBackendKwargs(
            max_age=0,
            session_cookie="yet_another_cookie_name",
            path="/yet/another/path",
            same_site="lax",
            https_only=False,
        ),
        CookieBackendKwargs(
            max_age=0,
            session_cookie="yet_another_cookie_name",
            path="/yet/another/path",
            same_site="none",
            https_only=False,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="yet_another_cookie_name",
            path="/another/path",
            same_site="strict",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="yet_another_cookie_name",
            path="/another/path",
            same_site="lax",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="yet_another_cookie_name",
            path="/another/path",
            same_site="none",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="yet_another_cookie_name",
            path="/another/path",
            same_site="strict",
            https_only=False,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="yet_another_cookie_name",
            path="/another/path",
            same_site="lax",
            https_only=False,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="yet_another_cookie_name",
            path="/another/path",
            same_site="none",
            https_only=False,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="yet_another_cookie_name",
            path="/yet/another/path",
            same_site="strict",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="yet_another_cookie_name",
            path="/yet/another/path",
            same_site="lax",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="yet_another_cookie_name",
            path="/yet/another/path",
            same_site="none",
            https_only=True,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="yet_another_cookie_name",
            path="/yet/another/path",
            same_site="strict",
            https_only=False,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="yet_another_cookie_name",
            path="/yet/another/path",
            same_site="lax",
            https_only=False,
        ),
        CookieBackendKwargs(
            max_age=1,
            session_cookie="yet_another_cookie_name",
            path="/yet/another/path",
            same_site="none",
            https_only=False,
        ),
    ]

    @pytest.mark.parametrize("kwargs", cookie_backend_kwargs)
    def test_parameterized_persist(self, kwargs: CookieBackendKwargs):
        cookie_backend = CookieStorageBackend(**kwargs)
        value = "somegarbage"
        scope = {"type": "http", "headers": []}
        cookie_backend.persist(scope, value)
        assert scope["type"] == "http"
        assert len(scope["headers"]) == 1
        assert isinstance(scope["headers"][0], tuple)
        assert scope["headers"][0][0] == "set-cookie".encode("latin-1")
        assert cookie_parser(scope["headers"][0][1].decode("latin-1")) == cookie_parser(
            f'{kwargs["session_cookie"]}={value}; path={kwargs["path"]};{" Max-Age=" + str(kwargs["max_age"]) + ";" if kwargs["max_age"] else ""} httponly; samesite={kwargs["same_site"]}{"" if kwargs["https_only"] is False else "; secure"}'
        )

    @pytest.mark.parametrize("kwargs", cookie_backend_kwargs)
    def test_parameterized_clear(self, kwargs: CookieBackendKwargs):
        cookie_backend = CookieStorageBackend(**kwargs)
        scope = {"type": "http", "headers": []}
        cookie_backend.clear(scope)
        assert scope["type"] == "http"
        assert len(scope["headers"]) == 1
        assert isinstance(scope["headers"][0], tuple)
        assert scope["headers"][0][0] == "set-cookie".encode("latin-1")
        assert cookie_parser(scope["headers"][0][1].decode("latin-1")) == cookie_parser(
            f'{kwargs["session_cookie"]}=null; path={kwargs["path"]}; expires=Thu, 01 Jan 1970 00:00:00 GMT; httponly; samesite={kwargs["same_site"]}{"" if kwargs["https_only"] is False else "; secure"}'
        )
