from time import sleep

import pytest

from starlette_session.middleware.codecbackends import CodecBackendInterface
from starlette_session.middleware.codecbackends.errors import DecodeError
from starlette_session.middleware.codecbackends.signer import SignerBackend


class TestSignerBackend:
    def test_is_expected_subclass(self):
        signer_backend = SignerBackend(key="superdupersecret")
        assert isinstance(signer_backend, CodecBackendInterface) is True

    def test_successful_decode(self):
        signer_backend = SignerBackend(key="superdupersecret")
        claims = {"test": "data"}
        token = signer_backend.encode(claims)
        assert signer_backend.decode(token) == claims

    def test_decode_after_max_age(self):
        signer_backend = SignerBackend(key="superdupersecret", max_age=0)
        claims = {"test": "data"}
        token = signer_backend.encode(claims)
        assert signer_backend.decode(token) == claims
        sleep(1)
        with pytest.raises(DecodeError):
            signer_backend.decode(token)
