from os import getenv

from c18_pytest.src.s13_conftest.netbox_api_handler import NetboxAPIHandler

# вот это общая проверка, её выносим в conftest
# test_netbox_url = getenv("TEST_NETBOX_URL")
# test_netbox_token = getenv("TEST_NETBOX_TOKEN")

# if not all((test_netbox_url, test_netbox_token)):
#     raise EnvironmentError("Тестовая среда не готова")


class TestNetboxAPIHandlerWithConftest:
    NETBOX_VERSION = "4.4.0"

    def test_get(self) -> None:
        test_netbox_url = getenv("TEST_NETBOX_URL")
        test_netbox_token = getenv("TEST_NETBOX_TOKEN")

        with NetboxAPIHandler(test_netbox_url, test_netbox_token) as netbox:
            response = netbox.get("/api/status/")
        assert isinstance(response, list)
        assert len(response) == 1
        assert response[0].get("netbox-version") == self.NETBOX_VERSION
