import typing

import pytest
from starlette.types import Message

from starlette_session.middleware.codecbackends import CodecBackendInterface


class TestCodecBackendInterface:
    def test_isinstance_behavior(self):
        class WithEncode:
            def encode(self, _: dict[str, typing.Any]) -> typing.Union[str, None]:
                return ""

        assert isinstance(WithEncode(), CodecBackendInterface) is False

        class WithDecode:
            def decode(self, _: str) -> dict[str, typing.Any]:
                return {}

        assert isinstance(WithDecode(), CodecBackendInterface) is False

        class DummyCodecBackend(WithEncode, WithDecode):
            pass

        assert isinstance(DummyCodecBackend(), CodecBackendInterface) is True

    def test_instantiation(self):
        with pytest.raises(TypeError):
            CodecBackendInterface()  # type: ignore

    def test_encode(self):
        class DummyCodecBackend(CodecBackendInterface):
            def encode(self, data: dict[str, typing.Any]):
                return super().encode(data)

            def decode(self, data: str):
                return super().decode(data)

        backend = DummyCodecBackend()
        with pytest.raises(NotImplementedError):
            backend.encode({})

    def test_decode(self):
        class DummyCodecBackend(CodecBackendInterface):
            def encode(self, data: dict[str, typing.Any]):
                return super().encode(data)

            def decode(self, data: str):
                return super().decode(data)

        backend = DummyCodecBackend()
        with pytest.raises(NotImplementedError):
            backend.decode("")
