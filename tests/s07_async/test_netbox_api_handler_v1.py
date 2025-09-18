# python -m unittest discover -s ./c18_pytest/src/s07_async/ -v
# export TEST_NETBOX_URL=https://demo.netbox.dev/ TEST_NETBOX_TOKEN=d5562616b529e6a121805ecadffaf5c2f48aeeac

from os import getenv
from unittest import IsolatedAsyncioTestCase, TestCase

from c18_pytest.src.s07_async.netbox_api_handler import NetboxAPIHandler


class NetboxAPIHandlerTestCase(TestCase):
    NETBOX_VERSION = "4.4.0"

    @classmethod
    def setUpClass(cls) -> None:
        test_netbox_url = getenv("TEST_NETBOX_URL")
        test_netbox_token = getenv("TEST_NETBOX_TOKEN")

        if not all((test_netbox_url, test_netbox_token)):
            raise EnvironmentError("Тестовая среда не готова")

        cls.netbox = NetboxAPIHandler(test_netbox_url, test_netbox_token)

    def test_get(self) -> None:
        with self.netbox:
            response = self.netbox.get("/api/status/")

        self.assertIsInstance(response, list)
        self.assertEqual(1, len(response))
        version = response[0].get("netbox-version")
        self.assertEqual(self.NETBOX_VERSION, version)


class NetboxAPIHandlerAsyncTestCase(IsolatedAsyncioTestCase):
    NETBOX_VERSION = "4.4.0"

    @classmethod
    def setUpClass(cls) -> None:
        test_netbox_url = getenv("TEST_NETBOX_URL")
        test_netbox_token = getenv("TEST_NETBOX_TOKEN")

        if not all((test_netbox_url, test_netbox_token)):
            raise EnvironmentError("Тестовая среда не готова")

        cls.netbox = NetboxAPIHandler(test_netbox_url, test_netbox_token)

    async def test_aget(self) -> None:
        async with self.netbox:
            response = await self.netbox.aget("/api/status/")

        self.assertIsInstance(response, list)
        self.assertEqual(1, len(response))
        version = response[0].get("netbox-version")
        self.assertEqual(self.NETBOX_VERSION, version)
