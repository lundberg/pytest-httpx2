# pytest-httpx2

A `pytest` plugin for mocking out `httpx2` using `respx`.

```py
import httpx2

def test_foobar(httpx2_mock: respx.Router) -> None:
    httpx2_mock.post("https://example.com/foobar").respond(201)
    response = httpx2.post("https://example.com/foobar")
    assert response.status_code == 201
```

## Configure using marker

```py
import pytest
import httpx2

@pytest.mark.httpx2(base_url="https://example.com")
def test_hamspam(httpx2_mock: respx.Router) -> None:
    httpx2_mock.get("/hamspam").respond(json={"id": 1337})
    response = httpx2.get("https://example.com/hamspam")
    assert response.status_code == 200
    assert response.json() == {"id": 1337}
```

See `respx` [documentation](https://lundberg.github.io/respx/guide/#base-url) for more
configuration options and api.
