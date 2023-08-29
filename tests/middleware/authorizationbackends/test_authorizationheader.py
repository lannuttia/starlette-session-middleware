import typing

import pytest
from starlette.requests import HTTPConnection

from starlette_session.middleware.authorizationbackends import (
    AuthorizationBackendInterface,
)
from starlette_session.middleware.authorizationbackends.authorizationheader import (
    AuthorizationHeaderAuthorizationBackend,
)


class TestAuthorizationHeaderAuthorizationBackend:
    def test_is_expected_subclass(self):
        authorization_header_authorization_backend = (
            AuthorizationHeaderAuthorizationBackend()
        )
        assert (
            isinstance(
                authorization_header_authorization_backend,
                AuthorizationBackendInterface,
            )
            is True
        )

    type_parameters = [
        "Bearer",
    ]

    @pytest.mark.parametrize("type", type_parameters)
    def test_authorization_header_exists(self, type):
        authorization_header_authorization_backend = (
            AuthorizationHeaderAuthorizationBackend(type=type)
        )
        token = "somegarbagetoken"
        authorization_header_value = f"{type} {token}"
        scope = {
            "type": "http",
            "headers": [
                [
                    "authorization".encode("latin-1"),
                    authorization_header_value.encode("latin-1"),
                ]
            ],
        }
        connection = HTTPConnection(scope=scope)
        assert authorization_header_authorization_backend.get_token(connection) == token

    @pytest.mark.parametrize("type", type_parameters)
    def test_authorization_header_case_insensitivity(self, type: str):
        authorization_header_authorization_backend = (
            AuthorizationHeaderAuthorizationBackend(type=type)
        )
        token = "somegarbagetoken"
        authorization_header_value = f"{type.lower()} {token}"
        scope = {
            "type": "http",
            "headers": [
                [
                    "authorization".encode("latin-1"),
                    authorization_header_value.encode("latin-1"),
                ]
            ],
        }
        connection = HTTPConnection(scope=scope)
        assert authorization_header_authorization_backend.get_token(connection) == token

    def test_mismatched_authorization_header_type(self):
        authorization_header_authorization_backend = (
            AuthorizationHeaderAuthorizationBackend(type="Bearer")
        )
        token = "somegarbagetoken"
        authorization_header_value = f"Basic {token}"
        scope = {
            "type": "http",
            "headers": [
                [
                    "authorization".encode("latin-1"),
                    authorization_header_value.encode("latin-1"),
                ]
            ],
        }
        connection = HTTPConnection(scope=scope)
        assert authorization_header_authorization_backend.get_token(connection) is None

    def test_no_authorization_header(self):
        authorization_header_authorization_backend = (
            AuthorizationHeaderAuthorizationBackend(type="Bearer")
        )
        scope = {
            "type": "http",
            "headers": [],
        }
        connection = HTTPConnection(scope=scope)
        assert authorization_header_authorization_backend.get_token(connection) is None
