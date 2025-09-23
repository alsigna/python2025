from unittest.mock import patch

from scrapli.driver.core import EOSDriver, IOSXEDriver

from c18_pytest.src.s12_testcase.device import Device


class TestDevice:
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
            assert version == expected_version
            device.cli.send_command.assert_called_once_with("show version")

    def test_scrapli_platform(self) -> None:
        device = Device("192.168.122.101", "cisco_iosxe")
        assert isinstance(device.cli, IOSXEDriver)
        # а тут тест должен падать
        # assert isinstance(device.cli, EOSDriver), "неправильный класс устройства"
