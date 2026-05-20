from textwrap import dedent
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from _pytest.pytester import Pytester


PYTESTER_CONFIG: Final = dedent(
    """
    [tool.pytest]
    addopts = ["-p pytest_httpx2"]
    """
)


def test_httpx2_mock_fixture(pytester: "Pytester") -> None:
    pytester.makepyfile("""
        import httpx2
        import pytest

        def test(httpx2_mock):
            route = httpx2_mock.get("https://example.com/") % 204
            response = httpx2.get("https://example.com/")
            assert response.status_code == 204
        """)
    pytester.makeini(PYTESTER_CONFIG)
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)


def test_httpx2_marker(pytester: "Pytester") -> None:
    pytester.makepyfile("""
        import httpx2
        import pytest

        @pytest.mark.httpx2(base_url="https://example.com", assert_all_mocked=False)
        def test(httpx2_mock):
            route = httpx2_mock.get("/path") % 204
            response = httpx2.get("https://example.com/path")
            assert response.status_code == 204
            response = httpx2.get("https://example.com/")
            assert response.status_code == 200
        """)
    pytester.makeini(PYTESTER_CONFIG)
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)
