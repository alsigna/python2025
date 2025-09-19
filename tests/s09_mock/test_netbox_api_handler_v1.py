# python -m unittest discover -s ./c18_pytest/src/s09_mock/ -v

from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import AsyncMock, MagicMock, patch

from c18_pytest.src.s09_mock.src.netbox_api_handler import NetboxAPIHandler


class NetboxAPIHandlerMixIn:
    NETBOX_VERSION = "4.3.6"

    @classmethod
    def setUpClass(cls) -> None:
        cls.netbox = NetboxAPIHandler("https://mock", "abcde")


class NetboxAPIHandlerTestCase(NetboxAPIHandlerMixIn, TestCase):
    @patch(
        target="c18_pytest.src.s09_mock.src.netbox_api_handler.httpx.Client",
        autospec=True,
    )
    def test_get(self, mock_client: MagicMock) -> None:
        # настраиваем мок-клиент, что бы в конструкциях вида
        # - with httpx.Client() as session:
        # - session = httpx.Client()
        # session была не настоящая, а мок-объектом
        mock_session = MagicMock()
        mock_client.return_value = mock_session

        # настраиваем мок-ответ, у которого мы используем
        # - .raise_for_status()
        # - .json()
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": [{"netbox-version": "4.3.6"}]}
        mock_response.raise_for_status.return_value = None
        # устанавливаем наш mock_response как значение для session.get()
        mock_session.get.return_value = mock_response

        with self.netbox:
            response = self.netbox.get("/api/status/")
        version = response[0].get("netbox-version")
        self.assertEqual(self.NETBOX_VERSION, version)


class NetboxAPIHandlerAsyncTestCase(NetboxAPIHandlerMixIn, IsolatedAsyncioTestCase):
    @patch(
        target="c18_pytest.src.s09_mock.src.netbox_api_handler.httpx.AsyncClient",
        autospec=True,
    )
    async def test_aget(self, mock_client) -> None:
        mock_session = MagicMock()
        # тут нужно использовать AsyncMock, потому, что async with self.netbox вызывает
        # __aexit__, в котором await self.session.aclose(), поэтому нужно сделать aclose
        # awaitable объектом
        mock_session.aclose = AsyncMock()
        mock_client.return_value = mock_session

        mock_response = MagicMock()
        mock_response.json.return_value = {"results": [{"netbox-version": "4.3.6"}]}
        mock_response.raise_for_status.return_value = None
        # и тут используем AsyncMock, аналогично aclose: используется await self.session.get()
        # поэтому get должен быть awaitable объектом
        mock_session.get = AsyncMock()
        mock_session.get.return_value = mock_response

        async with self.netbox:
            response = await self.netbox.aget("/api/status/")
        self.assertIsInstance(response, list)
        self.assertEqual(1, len(response))
        version = response[0].get("netbox-version")
        self.assertEqual(self.NETBOX_VERSION, version)
