import typing

from starlette.datastructures import MutableHeaders
from starlette.requests import HTTPConnection
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from starlette_session.middleware.codecbackends.errors import DecodeError
from starlette_session.middleware.codecbackends import CodecBackendInterface
from starlette_session.middleware.storagebackends import StorageBackendInterface
from starlette_session.middleware.authorizationbackends import (
    AuthorizationBackendInterface,
)


class SessionMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        codec_backend: CodecBackendInterface,
        storage_backend: StorageBackendInterface,
        authorization_backend: AuthorizationBackendInterface,
    ) -> None:
        self.app = app
        self.codec_backend = codec_backend
        self.storage_backend = storage_backend
        self.authorization_backend = authorization_backend

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):  # pragma: no cover
            await self.app(scope, receive, send)
            return

        connection = HTTPConnection(scope)
        initial_session_was_empty = True

        data = self.authorization_backend.get_token(connection)
        if data is not None:
            try:
                scope["session"] = self.codec_backend.decode(data)
                initial_session_was_empty = False
            except DecodeError:
                scope["session"] = {}
        else:
            scope["session"] = {}

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                if scope["session"]:
                    # We have session data to persist.
                    data = self.codec_backend.encode(scope["session"])
                    self.storage_backend.persist(message, data)
                elif not initial_session_was_empty:
                    # The session has been cleared.
                    self.storage_backend.clear(message)
            await send(message)

        await self.app(scope, receive, send_wrapper)
