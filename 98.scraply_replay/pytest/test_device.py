import pytest
from devices import CiscoDevice


@pytest.mark.parametrize(
    ("host", "expected_version"),
    [
        ("192.168.122.101", "17.03.03"),
        ("192.168.122.102", "15.9(3)M3"),
    ],
)
@pytest.mark.scrapli_replay
def test_cisco_get_version(host: str, expected_version: str):
    device = CiscoDevice(host)
    assert device.get_version() == expected_version
