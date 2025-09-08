# python -m unittest discover -s ./c18_pytest/src/s09_mock/ -v
from unittest import TestCase
from unittest.mock import AsyncMock, MagicMock, patch

from scrapli.response import Response

from c18_pytest.src.s09_mock.src.device import Device

# # пример с реальным устройством, без мокирования
# class RealDeviceTestCase(TestCase):
#     def test_get_version(self) -> None:
#         device = Device("192.168.122.101", "cisco_iosxe")
#         with device:
#             version = device.get_version()
#         expected_version = "17.3.3"
#         self.assertEqual(expected_version, version)


# пример с мокированием всего объекта Scrapli
class FullDeviceTestCase(TestCase):
    @patch(
        target="c18_pytest.src.s09_mock.src.device.Scrapli",
        spec=True,
    )
    def test_get_version(self, mock_scrapli: MagicMock) -> None:
        mock_cli = MagicMock()
        mock_cli.send_command.return_value.result = ", Version 17.3.3, RELEASE SOFTWARE (fc7)"
        mock_scrapli.return_value = mock_cli

        device = Device("192.168.122.101", "cisco_iosxe")
        with device:
            version = device.get_version()
        expected_version = "17.3.3"
        self.assertEqual(expected_version, version)
        mock_cli.send_command.assert_called_once_with("show version")


# пример с patch.object для того, что бы подменить только один метод send_command
class MethodDeviceTestCase(TestCase):
    def test_get_version(self) -> None:
        device = Device("192.168.122.101", "cisco_iosxe")
        with patch.object(
            target=device.cli,
            attribute="send_command",
            # return_value=MagicMock(result=", Version 17.3.3, RELEASE SOFTWARE (fc7)"),
            return_value=type(
                "Response",
                (),
                {"result": ", Version 17.3.3, RELEASE SOFTWARE (fc7)"},
            ),
        ):
            version = device.get_version()
            expected_version = "17.3.3"
            self.assertEqual(expected_version, version)
            device.cli.send_command.assert_called_once_with("show version")
            device.cli.send_command.assert_called_once_with("show version")
