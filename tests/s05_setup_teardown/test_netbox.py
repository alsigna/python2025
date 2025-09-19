# python -m unittest discover -s ./c18_pytest/src/s05_setup_teardown/
# python -m unittest discover -s ./c18_pytest/src/s05_setup_teardown/ -v
# export TEST_NETBOX_URL=https://demo.netbox.dev/ TEST_NETBOX_TOKEN=d5562616b529e6a121805ecadffaf5c2f48aeeac

from os import getenv
from unittest import TestCase

import httpx

# подготовка/очистка к тесту делается через setUp/tearDown
# создаем клиент, в самом тесте только логика, после теста подчищаем за собой


class NetboxTestCase(TestCase):
    NETBOX_VERSION = "4.4.1"
    PYTHON_VERSION = "3.12.3"
    QUEUE_COUNT = 3

    def setUp(self) -> None:
        test_netbox_url = getenv("TEST_NETBOX_URL")
        test_netbox_token = getenv("TEST_NETBOX_TOKEN")

        if not all((test_netbox_url, test_netbox_token)):
            raise EnvironmentError("Тестовая среда не готова")

        self.session = httpx.Client(
            transport=httpx.HTTPTransport(verify=False),
            base_url=test_netbox_url,
            headers={
                "Authorization": f"Token {test_netbox_token}",
                "Content-Type": "application/json",
                "Accept-Charset": "application/json",
                "User-Agent": "demo-python2025",
            },
        )

    def tearDown(self) -> None:
        self.session.close()

    def test_versions(self) -> None:
        response = self.session.get("/api/status/")
        response.raise_for_status()
        response_json = response.json()

        netbox_version = response_json.get("netbox-version", "")
        self.assertEqual(self.NETBOX_VERSION, netbox_version)

    def test_background_queues_count(self) -> None:
        response = self.session.get("/api/core/background-queues/")
        response.raise_for_status()
        response_json = response.json()

        queue_count = response_json.get("count")
        self.assertEqual(self.QUEUE_COUNT, queue_count)
