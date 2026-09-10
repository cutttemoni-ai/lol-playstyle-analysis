from __future__ import annotations

import httpx
import pytest

from riot_api.client import RiotAPIClient, RiotAPIError


def test_429_uses_retry_after_and_then_succeeds(monkeypatch):
    sleeps = []
    attempts = 0

    def handler(request):
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            return httpx.Response(429, headers={"Retry-After": "2"})
        return httpx.Response(200, json={"ok": True})

    monkeypatch.setattr("riot_api.client.time.sleep", sleeps.append)
    with RiotAPIClient(
        "test-key", request_interval=0, transport=httpx.MockTransport(handler)
    ) as client:
        assert client.get_json("https://example.test") == {"ok": True}
    assert 2.0 in sleeps
    assert attempts == 2


def test_server_errors_retry_at_most_three_times(monkeypatch):
    attempts = 0

    def handler(request):
        nonlocal attempts
        attempts += 1
        return httpx.Response(503)

    monkeypatch.setattr("riot_api.client.time.sleep", lambda _: None)
    with RiotAPIClient(
        "test-key", request_interval=0, max_retries=3, transport=httpx.MockTransport(handler)
    ) as client:
        with pytest.raises(RiotAPIError) as caught:
            client.get_json("https://example.test")
    assert caught.value.status_code == 503
    assert caught.value.retries == 3
    assert attempts == 4


@pytest.mark.parametrize(
    ("status", "message"),
    [
        (401, "올바르지"),
        (403, "만료"),
        (404, "찾을 수 없"),
    ],
)
def test_actionable_http_errors_do_not_expose_key(status, message):
    transport = httpx.MockTransport(lambda request: httpx.Response(status))
    with RiotAPIClient("test-key-super-secret", request_interval=0, transport=transport) as client:
        with pytest.raises(RiotAPIError) as caught:
            client.get_json("https://example.test")
    assert message in str(caught.value)
    assert "test-key-super-secret" not in str(caught.value)
