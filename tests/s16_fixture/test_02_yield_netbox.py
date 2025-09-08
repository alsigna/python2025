from collections.abc import Iterator
from os import getenv

import httpx
import pytest

NETBOX_VERSION = "4.4.0"
PYTHON_VERSION = "3.12.3"
QUEUE_COUNT = 3


@pytest.fixture()
def session() -> Iterator[httpx.Client]:
    test_netbox_url = getenv("TEST_NETBOX_URL", "")
    test_netbox_token = getenv("TEST_NETBOX_TOKEN", "")

    with httpx.Client(
        transport=httpx.HTTPTransport(verify=False),
        base_url=test_netbox_url,
        headers={
            "Authorization": f"Token {test_netbox_token}",
            "Content-Type": "application/json",
            "Accept-Charset": "application/json",
            "User-Agent": "demo-python2025",
        },
    ) as client:
        yield client

    # with httpx.Client() as client:
    #     yield client
    #
    # лучше, чем
    #
    # client = httpx.Client()
    # yield client
    # client.close()


def test_versions(session: httpx.Client) -> None:
    response = session.get("/api/status/")
    response.raise_for_status()
    response_json = response.json()
    netbox_version = response_json.get("netbox-version", "")

    assert netbox_version == NETBOX_VERSION


def test_background_queues_count(session: httpx.Client) -> None:
    response = session.get("/api/core/background-queues/")
    response.raise_for_status()
    response_json = response.json()
    queue_count = response_json.get("count")

    assert queue_count == QUEUE_COUNT
