from os import getenv

import pytest


def check_netbox_env() -> None:
    test_netbox_url = getenv("TEST_NETBOX_URL")
    test_netbox_token = getenv("TEST_NETBOX_TOKEN")
    # test_netbox_token = None

    if not all((test_netbox_url, test_netbox_token)):
        pytest.exit("Тестовая среда не готова")


check_netbox_env()
