from datetime import datetime, timedelta
from time import sleep

import pytest

from starlette_session.middleware.codecbackends import CodecBackendInterface
from starlette_session.middleware.codecbackends.errors import DecodeError
from starlette_session.middleware.codecbackends.jwt import JwtBackend


class TestJwtBackend:
    algorithms = [
        "HS256",
        "HS384",
        "HS512",
    ]

    @pytest.mark.parametrize("algorithm", algorithms)
    def test_is_expected_subclass(self, algorithm):
        jwt_backend = JwtBackend(key="superdupersecret", algorithm=algorithm)
        assert isinstance(jwt_backend, CodecBackendInterface) is True

    @pytest.mark.parametrize("algorithm", algorithms)
    def test_successful_decode(self, algorithm):
        jwt_backend = JwtBackend(key="superdupersecret", algorithm=algorithm)
        claims = {"test": "data"}
        token = jwt_backend.encode(claims)
        assert jwt_backend.decode(token) == claims

    @pytest.mark.parametrize("algorithm", algorithms)
    def test_exp_claim_in_past(self, algorithm):
        jwt_backend = JwtBackend(key="superdupersecret", algorithm=algorithm)
        one_second_from_now = datetime.now() + timedelta(seconds=1)
        exp = datetime.timestamp(one_second_from_now)
        claims = {"test": "data", "exp": exp}
        token = jwt_backend.encode(claims)
        assert jwt_backend.decode(token) == claims
        sleep(1)
        with pytest.raises(DecodeError):
            jwt_backend.decode(token)

    @pytest.mark.parametrize("algorithm", algorithms)
    def test_nbf_claim_in_future(self, algorithm):
        jwt_backend = JwtBackend(key="superdupersecret", algorithm=algorithm)
        one_second_from_now = datetime.now() + timedelta(seconds=1)
        nbf = datetime.timestamp(one_second_from_now)
        claims = {"test": "data", "nbf": nbf}
        token = jwt_backend.encode(claims)
        with pytest.raises(DecodeError):
            jwt_backend.decode(token)
        sleep(1)
        assert jwt_backend.decode(token) == claims

    @pytest.mark.parametrize("algorithm", algorithms)
    def test_exp_and_nbf_window(self, algorithm):
        jwt_backend = JwtBackend(key="superdupersecret", algorithm=algorithm)
        one_second_from_now = datetime.now() + timedelta(seconds=1)
        two_seconds_from_now = one_second_from_now + timedelta(seconds=1)
        nbf = datetime.timestamp(one_second_from_now)
        exp = datetime.timestamp(two_seconds_from_now)
        claims = {"test": "data", "nbf": nbf, "exp": exp}
        token = jwt_backend.encode(claims)
        with pytest.raises(DecodeError):
            jwt_backend.decode(token)
        sleep(1)
        assert jwt_backend.decode(token) == claims
        sleep(1)
        with pytest.raises(DecodeError):
            jwt_backend.decode(token)
