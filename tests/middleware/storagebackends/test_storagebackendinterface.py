import pytest
from starlette.types import Message

from starlette_session.middleware.storagebackends import StorageBackendInterface


class TestStorageBackendInterface:
    def test_isinstance_behavior(self):
        class WithPersist:
            def persist(self, message: Message, data: str) -> None:
                return None

        assert isinstance(WithPersist(), StorageBackendInterface) is False

        class WithClear:
            def clear(self, message: Message) -> None:
                return None

        assert isinstance(WithClear(), StorageBackendInterface) is False

        class DummyStorageBackend(WithPersist, WithClear):
            pass

        assert isinstance(DummyStorageBackend(), StorageBackendInterface) is True

    def test_instantiation(self):
        with pytest.raises(TypeError):
            StorageBackendInterface()  # type: ignore

    def test_persist(self):
        class DummyStorageBackend(StorageBackendInterface):
            def persist(self, message: Message, data: str):
                return super().persist(message, data)

            def clear(self, message: Message):
                return super().clear(message)

        backend = DummyStorageBackend()
        scope = {
            "type": "http",
        }
        with pytest.raises(NotImplementedError):
            backend.persist(scope, "")

    def test_clear(self):
        class DummyStorageBackend(StorageBackendInterface):
            def persist(self, message: Message, data: str):
                return super().persist(message, data)

            def clear(self, message: Message):
                return super().clear(message)

        backend = DummyStorageBackend()
        scope = {
            "type": "http",
        }
        with pytest.raises(NotImplementedError):
            backend.clear(scope)
