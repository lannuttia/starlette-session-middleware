import re
from datetime import datetime, timedelta
from time import sleep

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route
from starlette.testclient import TestClient

from starlette_session.middleware import SessionMiddleware
from starlette_session.middleware.authorizationbackends.authorizationheader import (
    AuthorizationHeaderAuthorizationBackend,
)
from starlette_session.middleware.authorizationbackends.cookie import (
    CookieAuthorizationBackend,
)
from starlette_session.middleware.codecbackends.jwt import JwtCodecBackend
from starlette_session.middleware.codecbackends.signer import SignerCodecBackend
from starlette_session.middleware.storagebackends.cookie import CookieStorageBackend


def view_session(request):
    return JSONResponse({"session": request.session})


async def update_session(request):
    data = await request.json()
    request.session.update(data)
    return JSONResponse({"session": request.session})


async def clear_session(request):
    request.session.clear()
    return JSONResponse({"session": request.session})


class TestJwtBackendWithAuthorizationHeaderAuthorization:
    def test_session(self, test_client_factory):
        app = Starlette(
            routes=[
                Route("/view_session", endpoint=view_session),
                Route("/update_session", endpoint=update_session, methods=["POST"]),
                Route("/clear_session", endpoint=clear_session, methods=["POST"]),
            ],
            middleware=[
                Middleware(
                    SessionMiddleware,
                    codec_backend=JwtCodecBackend(key="example", algorithm="HS256"),
                    storage_backend=CookieStorageBackend(),
                    authorization_backend=AuthorizationHeaderAuthorizationBackend(),
                )
            ],
        )
        client = test_client_factory(app)

        response = client.get("/view_session")
        assert response.json() == {"session": {}}

        now = datetime.now()
        exp = datetime.timestamp(now + timedelta(days=14))
        response = client.post("/update_session", json={"exp": exp, "some": "data"})
        assert response.json() == {"session": {"exp": exp, "some": "data"}}

        # check cookie max-age
        set_cookie = response.headers["set-cookie"]
        max_age_matches = re.search(r"; Max-Age=(\d+);", set_cookie)
        assert max_age_matches is not None
        assert int(max_age_matches[1]) == int(14 * 24 * 3600)
        token = re.search(r"session=([^;]*);", response.headers["set-cookie"])[1]

        response = client.get(
            "/view_session",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        assert response.json() == {"session": {"exp": exp, "some": "data"}}

        response = client.post(
            "/clear_session",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        assert response.json() == {"session": {}}
        token = re.search(r"session=([^;]*);", response.headers["set-cookie"])[1]

        response = client.get(
            "/view_session",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        assert response.json() == {"session": {}}

    def test_session_expires(self, test_client_factory):
        app = Starlette(
            routes=[
                Route("/view_session", endpoint=view_session),
                Route("/update_session", endpoint=update_session, methods=["POST"]),
            ],
            middleware=[
                Middleware(
                    SessionMiddleware,
                    codec_backend=JwtCodecBackend(key="example", algorithm="HS256"),
                    storage_backend=CookieStorageBackend(),
                    authorization_backend=AuthorizationHeaderAuthorizationBackend(),
                )
            ],
        )
        client = test_client_factory(app)

        now = datetime.now()
        exp = datetime.timestamp(now + timedelta(seconds=1))
        response = client.post("/update_session", json={"exp": exp, "some": "data"})
        assert response.json() == {"session": {"exp": exp, "some": "data"}}
        token = re.search(r"session=([^;]*);", response.headers["set-cookie"])[1]
        response = client.get(
            "/view_session", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.json() == {"session": {"exp": exp, "some": "data"}}
        sleep(1)
        response = client.get(
            "/view_session", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.json() == {"session": {}}

    def test_session_future_nbf(self, test_client_factory):
        app = Starlette(
            routes=[
                Route("/view_session", endpoint=view_session),
                Route("/update_session", endpoint=update_session, methods=["POST"]),
            ],
            middleware=[
                Middleware(
                    SessionMiddleware,
                    codec_backend=JwtCodecBackend(key="example", algorithm="HS256"),
                    storage_backend=CookieStorageBackend(),
                    authorization_backend=AuthorizationHeaderAuthorizationBackend(),
                )
            ],
        )
        client = test_client_factory(app)

        now = datetime.now()
        nbf = datetime.timestamp(now + timedelta(seconds=30))
        response = client.post("/update_session", json={"nbf": nbf, "some": "data"})
        assert response.json() == {"session": {"nbf": nbf, "some": "data"}}
        token = re.search(r"session=([^;]*);", response.headers["set-cookie"])[1]
        response = client.get(
            "/view_session",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        assert response.json() == {"session": {}}
        sleep(1)
        response = client.post("/update_session", json={"nbf": nbf, "some": "data"})
        assert response.json() == {"session": {"nbf": nbf, "some": "data"}}
        token = re.search(r"session=([^;]*);", response.headers["set-cookie"])[1]
        response = client.get(
            "/view_session",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        assert response.json() == {"session": {"nbf": nbf, "some": "data"}}

    def test_session_cookie_subpath(self, test_client_factory):
        second_app = Starlette(
            routes=[
                Route("/update_session", endpoint=update_session, methods=["POST"]),
            ],
            middleware=[
                Middleware(
                    SessionMiddleware,
                    codec_backend=JwtCodecBackend(key="example", algorithm="HS256"),
                    storage_backend=CookieStorageBackend(path="/second_app"),
                    authorization_backend=AuthorizationHeaderAuthorizationBackend(),
                )
            ],
        )
        app = Starlette(routes=[Mount("/second_app", app=second_app)])
        client = test_client_factory(app, base_url="http://testserver/second_app")
        response = client.post("/update_session", json={"some": "data"})
        assert response.status_code == 200
        cookie = response.headers["set-cookie"]
        cookie_path_match = re.search(r"; path=(\S+);", cookie)
        assert cookie_path_match is not None
        cookie_path = cookie_path_match.groups()[0]
        assert cookie_path == "/second_app"

    def test_invalid_session_cookie(self, test_client_factory):
        app = Starlette(
            routes=[
                Route("/view_session", endpoint=view_session),
                Route("/update_session", endpoint=update_session, methods=["POST"]),
            ],
            middleware=[
                Middleware(
                    SessionMiddleware,
                    codec_backend=JwtCodecBackend(key="example", algorithm="HS256"),
                    storage_backend=CookieStorageBackend(),
                    authorization_backend=AuthorizationHeaderAuthorizationBackend(),
                )
            ],
        )
        client = test_client_factory(app)

        response = client.post("/update_session", json={"some": "data"})
        assert response.json() == {"session": {"some": "data"}}

        # we expect it to not raise an exception if we provide a bogus session cookie
        client = test_client_factory(app, headers={"Authorization": "invalid"})
        response = client.get("/view_session")
        assert response.json() == {"session": {}}


class TestJwtBackendWithCookieAuthorization:
    def test_session(self, test_client_factory):
        app = Starlette(
            routes=[
                Route("/view_session", endpoint=view_session),
                Route("/update_session", endpoint=update_session, methods=["POST"]),
                Route("/clear_session", endpoint=clear_session, methods=["POST"]),
            ],
            middleware=[
                Middleware(
                    SessionMiddleware,
                    codec_backend=JwtCodecBackend(key="example", algorithm="HS256"),
                    storage_backend=CookieStorageBackend(),
                    authorization_backend=CookieAuthorizationBackend(),
                )
            ],
        )
        client = test_client_factory(app)

        response = client.get("/view_session")
        assert response.json() == {"session": {}}

        now = datetime.now()
        exp = datetime.timestamp(now + timedelta(days=14))
        response = client.post("/update_session", json={"exp": exp, "some": "data"})
        assert response.json() == {"session": {"exp": exp, "some": "data"}}

        # check cookie max-age
        set_cookie = response.headers["set-cookie"]
        max_age_matches = re.search(r"; Max-Age=(\d+);", set_cookie)
        assert max_age_matches is not None
        assert int(max_age_matches[1]) == int(14 * 24 * 3600)

        response = client.get("/view_session")
        assert response.json() == {"session": {"exp": exp, "some": "data"}}

        response = client.post("/clear_session")
        assert response.json() == {"session": {}}

        response = client.get("/view_session")
        assert response.json() == {"session": {}}

    def test_session_expires(self, test_client_factory):
        app = Starlette(
            routes=[
                Route("/view_session", endpoint=view_session),
                Route("/update_session", endpoint=update_session, methods=["POST"]),
            ],
            middleware=[
                Middleware(
                    SessionMiddleware,
                    codec_backend=JwtCodecBackend(key="example", algorithm="HS256"),
                    storage_backend=CookieStorageBackend(),
                    authorization_backend=CookieAuthorizationBackend(),
                )
            ],
        )
        client = test_client_factory(app)

        now = datetime.now()
        exp = datetime.timestamp(now + timedelta(seconds=1))
        response = client.post("/update_session", json={"exp": exp, "some": "data"})
        assert response.json() == {"session": {"exp": exp, "some": "data"}}
        response = client.get("/view_session")
        assert response.json() == {"session": {"exp": exp, "some": "data"}}
        sleep(1)
        response = client.get("/view_session")
        assert response.json() == {"session": {}}

    def test_session_future_nbf(self, test_client_factory):
        app = Starlette(
            routes=[
                Route("/view_session", endpoint=view_session),
                Route("/update_session", endpoint=update_session, methods=["POST"]),
            ],
            middleware=[
                Middleware(
                    SessionMiddleware,
                    codec_backend=JwtCodecBackend(key="example", algorithm="HS256"),
                    storage_backend=CookieStorageBackend(),
                    authorization_backend=CookieAuthorizationBackend(),
                )
            ],
        )
        client = test_client_factory(app)

        now = datetime.now()
        nbf = datetime.timestamp(now + timedelta(seconds=1))
        response = client.post("/update_session", json={"nbf": nbf, "some": "data"})
        assert response.json() == {"session": {"nbf": nbf, "some": "data"}}
        response = client.get("/view_session")
        assert response.json() == {"session": {}}
        sleep(1)
        response = client.post("/update_session", json={"nbf": nbf, "some": "data"})
        assert response.json() == {"session": {"nbf": nbf, "some": "data"}}
        response = client.get("/view_session")
        assert response.json() == {"session": {"nbf": nbf, "some": "data"}}

    def test_secure_session(self, test_client_factory):
        app = Starlette(
            routes=[
                Route("/view_session", endpoint=view_session),
                Route("/update_session", endpoint=update_session, methods=["POST"]),
                Route("/clear_session", endpoint=clear_session, methods=["POST"]),
            ],
            middleware=[
                Middleware(
                    SessionMiddleware,
                    codec_backend=JwtCodecBackend(key="example", algorithm="HS256"),
                    storage_backend=CookieStorageBackend(https_only=True),
                    authorization_backend=CookieAuthorizationBackend(),
                )
            ],
        )
        secure_client = test_client_factory(app, base_url="https://testserver")
        unsecure_client = test_client_factory(app, base_url="http://testserver")

        response = unsecure_client.get("/view_session")
        assert response.json() == {"session": {}}

        response = unsecure_client.post("/update_session", json={"some": "data"})
        assert response.json() == {"session": {"some": "data"}}

        response = unsecure_client.get("/view_session")
        assert response.json() == {"session": {}}

        response = secure_client.get("/view_session")
        assert response.json() == {"session": {}}

        response = secure_client.post("/update_session", json={"some": "data"})
        assert response.json() == {"session": {"some": "data"}}

        response = secure_client.get("/view_session")
        assert response.json() == {"session": {"some": "data"}}

        response = secure_client.post("/clear_session")
        assert response.json() == {"session": {}}

        response = secure_client.get("/view_session")
        assert response.json() == {"session": {}}

    def test_session_cookie_subpath(self, test_client_factory):
        second_app = Starlette(
            routes=[
                Route("/update_session", endpoint=update_session, methods=["POST"]),
            ],
            middleware=[
                Middleware(
                    SessionMiddleware,
                    codec_backend=JwtCodecBackend(key="example", algorithm="HS256"),
                    storage_backend=CookieStorageBackend(path="/second_app"),
                    authorization_backend=CookieAuthorizationBackend(),
                )
            ],
        )
        app = Starlette(routes=[Mount("/second_app", app=second_app)])
        client = test_client_factory(app, base_url="http://testserver/second_app")
        response = client.post("/update_session", json={"some": "data"})
        assert response.status_code == 200
        cookie = response.headers["set-cookie"]
        cookie_path_match = re.search(r"; path=(\S+);", cookie)
        assert cookie_path_match is not None
        cookie_path = cookie_path_match.groups()[0]
        assert cookie_path == "/second_app"

    def test_invalid_session_cookie(self, test_client_factory):
        app = Starlette(
            routes=[
                Route("/view_session", endpoint=view_session),
                Route("/update_session", endpoint=update_session, methods=["POST"]),
            ],
            middleware=[
                Middleware(
                    SessionMiddleware,
                    codec_backend=JwtCodecBackend(key="example", algorithm="HS256"),
                    storage_backend=CookieStorageBackend(),
                    authorization_backend=CookieAuthorizationBackend(),
                )
            ],
        )
        client = test_client_factory(app)

        response = client.post("/update_session", json={"some": "data"})
        assert response.json() == {"session": {"some": "data"}}

        # we expect it to not raise an exception if we provide a bogus session cookie
        client = test_client_factory(app, cookies={"session": "invalid"})
        response = client.get("/view_session")
        assert response.json() == {"session": {}}

    def test_session_cookie(self, test_client_factory):
        app = Starlette(
            routes=[
                Route("/view_session", endpoint=view_session),
                Route("/update_session", endpoint=update_session, methods=["POST"]),
            ],
            middleware=[
                Middleware(
                    SessionMiddleware,
                    codec_backend=JwtCodecBackend(key="example", algorithm="HS256"),
                    storage_backend=CookieStorageBackend(max_age=None),
                    authorization_backend=CookieAuthorizationBackend(),
                )
            ],
        )
        client: TestClient = test_client_factory(app)

        response = client.post("/update_session", json={"some": "data"})
        assert response.json() == {"session": {"some": "data"}}

        # check cookie max-age
        set_cookie = response.headers["set-cookie"]
        assert "Max-Age" not in set_cookie

        client.cookies.delete("session")
        response = client.get("/view_session")
        assert response.json() == {"session": {}}


class TestSignerBackendWithCookieAuthorization:
    def test_session(self, test_client_factory):
        app = Starlette(
            routes=[
                Route("/view_session", endpoint=view_session),
                Route("/update_session", endpoint=update_session, methods=["POST"]),
                Route("/clear_session", endpoint=clear_session, methods=["POST"]),
            ],
            middleware=[
                Middleware(
                    SessionMiddleware,
                    codec_backend=SignerCodecBackend(key="example"),
                    storage_backend=CookieStorageBackend(),
                    authorization_backend=CookieAuthorizationBackend(),
                )
            ],
        )
        client = test_client_factory(app)

        response = client.get("/view_session")
        assert response.json() == {"session": {}}

        response = client.post("/update_session", json={"some": "data"})
        assert response.json() == {"session": {"some": "data"}}

        # check cookie max-age
        set_cookie = response.headers["set-cookie"]
        max_age_matches = re.search(r"; Max-Age=(\d+);", set_cookie)
        assert max_age_matches is not None
        assert int(max_age_matches[1]) == 14 * 24 * 3600

        response = client.get("/view_session")
        assert response.json() == {"session": {"some": "data"}}

        response = client.post("/clear_session")
        assert response.json() == {"session": {}}

        response = client.get("/view_session")
        assert response.json() == {"session": {}}

    def test_session_expires(self, test_client_factory):
        app = Starlette(
            routes=[
                Route("/view_session", endpoint=view_session),
                Route("/update_session", endpoint=update_session, methods=["POST"]),
            ],
            middleware=[
                Middleware(
                    SessionMiddleware,
                    codec_backend=SignerCodecBackend(key="example", max_age=-1),
                    storage_backend=CookieStorageBackend(max_age=-1),
                    authorization_backend=CookieAuthorizationBackend(),
                )
            ],
        )
        client = test_client_factory(app)

        response = client.post("/update_session", json={"some": "data"})
        assert response.json() == {"session": {"some": "data"}}

        # requests removes expired cookies from response.cookies, we need to
        # fetch session id from the headers and pass it explicitly
        expired_cookie_header = response.headers["set-cookie"]
        expired_session_match = re.search(r"session=([^;]*);", expired_cookie_header)
        assert expired_session_match is not None
        expired_session_value = expired_session_match[1]
        client = test_client_factory(app, cookies={"session": expired_session_value})
        response = client.get("/view_session")
        assert response.json() == {"session": {}}

    def test_secure_session(self, test_client_factory):
        app = Starlette(
            routes=[
                Route("/view_session", endpoint=view_session),
                Route("/update_session", endpoint=update_session, methods=["POST"]),
                Route("/clear_session", endpoint=clear_session, methods=["POST"]),
            ],
            middleware=[
                Middleware(
                    SessionMiddleware,
                    codec_backend=SignerCodecBackend(key="example"),
                    storage_backend=CookieStorageBackend(https_only=True),
                    authorization_backend=CookieAuthorizationBackend(),
                )
            ],
        )
        secure_client = test_client_factory(app, base_url="https://testserver")
        unsecure_client = test_client_factory(app, base_url="http://testserver")

        response = unsecure_client.get("/view_session")
        assert response.json() == {"session": {}}

        response = unsecure_client.post("/update_session", json={"some": "data"})
        assert response.json() == {"session": {"some": "data"}}

        response = unsecure_client.get("/view_session")
        assert response.json() == {"session": {}}

        response = secure_client.get("/view_session")
        assert response.json() == {"session": {}}

        response = secure_client.post("/update_session", json={"some": "data"})
        assert response.json() == {"session": {"some": "data"}}

        response = secure_client.get("/view_session")
        assert response.json() == {"session": {"some": "data"}}

        response = secure_client.post("/clear_session")
        assert response.json() == {"session": {}}

        response = secure_client.get("/view_session")
        assert response.json() == {"session": {}}

    def test_session_cookie_subpath(self, test_client_factory):
        second_app = Starlette(
            routes=[
                Route("/update_session", endpoint=update_session, methods=["POST"]),
            ],
            middleware=[
                Middleware(
                    SessionMiddleware,
                    codec_backend=SignerCodecBackend(key="example"),
                    storage_backend=CookieStorageBackend(path="/second_app"),
                    authorization_backend=CookieAuthorizationBackend(),
                )
            ],
        )
        app = Starlette(routes=[Mount("/second_app", app=second_app)])
        client = test_client_factory(app, base_url="http://testserver/second_app")
        response = client.post("/update_session", json={"some": "data"})
        assert response.status_code == 200
        cookie = response.headers["set-cookie"]
        cookie_path_match = re.search(r"; path=(\S+);", cookie)
        assert cookie_path_match is not None
        cookie_path = cookie_path_match.groups()[0]
        assert cookie_path == "/second_app"

    def test_invalid_session_cookie(self, test_client_factory):
        app = Starlette(
            routes=[
                Route("/view_session", endpoint=view_session),
                Route("/update_session", endpoint=update_session, methods=["POST"]),
            ],
            middleware=[
                Middleware(
                    SessionMiddleware,
                    codec_backend=SignerCodecBackend(key="example"),
                    storage_backend=CookieStorageBackend(),
                    authorization_backend=CookieAuthorizationBackend(),
                )
            ],
        )
        client = test_client_factory(app)

        response = client.post("/update_session", json={"some": "data"})
        assert response.json() == {"session": {"some": "data"}}

        # we expect it to not raise an exception if we provide a bogus session cookie
        client = test_client_factory(app, cookies={"session": "invalid"})
        response = client.get("/view_session")
        assert response.json() == {"session": {}}

    def test_session_cookie(self, test_client_factory):
        app = Starlette(
            routes=[
                Route("/view_session", endpoint=view_session),
                Route("/update_session", endpoint=update_session, methods=["POST"]),
            ],
            middleware=[
                Middleware(
                    SessionMiddleware,
                    codec_backend=SignerCodecBackend(key="example", max_age=None),
                    storage_backend=CookieStorageBackend(max_age=None),
                    authorization_backend=CookieAuthorizationBackend(),
                )
            ],
        )
        client: TestClient = test_client_factory(app)

        response = client.post("/update_session", json={"some": "data"})
        assert response.json() == {"session": {"some": "data"}}

        # check cookie max-age
        set_cookie = response.headers["set-cookie"]
        assert "Max-Age" not in set_cookie

        client.cookies.delete("session")
        response = client.get("/view_session")
        assert response.json() == {"session": {}}
