# python -m unittest discover -s ./c18_pytest/src/s09_mock/ -v
from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import AsyncMock, MagicMock, patch

from c18_pytest.src.s09_mock.src.netbox_api_handler import NetboxAPIHandler


# тут общую часть вынесли в mixin
class NetboxAPIMockMixin:
    NETBOX_VERSION = "4.3.6"

    @classmethod
    def create_mock_session(cls) -> MagicMock:
        if IsolatedAsyncioTestCase in cls.__mro__:
            async_mode = True
        else:
            async_mode = False

        session = MagicMock()
        if async_mode:
            session.get = AsyncMock()
            session.post = AsyncMock()
            session.aclose = AsyncMock()
        else:
            session.get = MagicMock()
            session.post = MagicMock()

        response = MagicMock()
        response.json.return_value = {"results": [{"netbox-version": "4.3.6"}]}
        response.raise_for_status.return_value = None

        session.get.return_value = response
        session.post.return_value = response  # у post другой ответ, но для примера

        return session

    @classmethod
    def setUpClass(cls) -> None:
        cls.mock_session = cls.create_mock_session()
        cls.netbox = NetboxAPIHandler("https://mock", "token")


class NetboxAPIHandlerTestCase(NetboxAPIMockMixin, TestCase):
    @patch(
        target="c18_pytest.src.s09_mock.src.netbox_api_handler.httpx.Client",
        autospec=True,
    )
    def test_get(self, mock_client: MagicMock) -> None:
        mock_client.return_value = self.mock_session
        with self.netbox:
            response = self.netbox.get("/api/status/")
        assert response[0]["netbox-version"] == self.NETBOX_VERSION

    # @patch(
    #     target="c18_pytest.src.s09_mock.src.netbox_api_handler.httpx.Client",
    #     autospec=True,
    # )
    # def test_post(self, mock_client: MagicMock) -> None:
    #     mock_client.return_value = self.mock_session
    #     with self.netbox:
    #         response = self.netbox.post("/api/status/")
    #     assert response[0]["netbox-version"] == self.NETBOX_VERSION


class NetboxAPIHandlerAsyncTestCase(NetboxAPIMockMixin, IsolatedAsyncioTestCase):
    @patch(
        target="c18_pytest.src.s09_mock.src.netbox_api_handler.httpx.AsyncClient",
        autospec=True,
    )
    async def test_aget(self, mock_client: MagicMock) -> None:
        mock_client.return_value = self.mock_session
        async with self.netbox:
            response = await self.netbox.aget("/api/status/")
        assert response[0]["netbox-version"] == self.NETBOX_VERSION

    # @patch(
    #     target="c18_pytest.src.s09_mock.src.netbox_api_handler.httpx.AsyncClient",
    #     autospec=True,
    # )
    # async def test_apost(self, mock_client: MagicMock) -> None:
    #     mock_client.return_value = self.mock_session
    #     async with self.netbox:
    #         response = await self.netbox.aget("/api/status/")
    #     assert response[0]["netbox-version"] == self.NETBOX_VERSION
    #     assert response[0]["netbox-version"] == self.NETBOX_VERSION
