from collections.abc import Generator

import pytest
import respx
from respx.mocks import HTTPCoreMocker


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "httpx2(*, assert_all_called=False, assert_all_mocked=False, base_url=...): "
        "configure the httpx2_mock fixture. "
        "See https://lundberg.github.io/respx/api.html#configuration",
    )


@pytest.fixture
def httpx2_mock(request: pytest.FixtureRequest) -> Generator[respx.Router, None, None]:
    options = {}
    if (marker := request.node.get_closest_marker("httpx2")) is not None:
        options.update(marker.kwargs)
    options.setdefault("using", "httpcore2")
    with respx.mock(**options) as router:
        yield router


class HTTPCore2Mocker(HTTPCoreMocker):
    name = "httpcore2"
    targets = [
        "httpcore2._sync.connection.HTTPConnection",
        "httpcore2._sync.connection_pool.ConnectionPool",
        "httpcore2._sync.http_proxy.HTTPProxy",
        "httpcore2._async.connection.AsyncHTTPConnection",
        "httpcore2._async.connection_pool.AsyncConnectionPool",
        "httpcore2._async.http_proxy.AsyncHTTPProxy",
    ]
