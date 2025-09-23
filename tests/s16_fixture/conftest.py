from os import getenv

import pytest


def check_netbox_env() -> None:
    test_netbox_url = getenv("TEST_NETBOX_URL")
    test_netbox_token = getenv("TEST_NETBOX_TOKEN")
    # test_netbox_token = None

    if not all((test_netbox_url, test_netbox_token)):
        pytest.exit("Тестовая среда не готова")


check_netbox_env()


@pytest.fixture(scope="session", autouse=True)
def check_redis_env() -> bool:
    test_redis_host = getenv("TEST_REDIS_HOST")
    test_redis_port = getenv("TEST_REDIS_PORT")
    if not all((test_redis_host, test_redis_port)):
        pytest.exit("Тестовая среда не готова")
