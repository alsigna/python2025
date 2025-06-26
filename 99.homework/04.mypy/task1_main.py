# - нужно сделать pyi файл (вручную или автоматически) для task1_legacy_code
# - довести его до рабочего состояния
# - импортировать craft_nb_query в task1_main.py из task1_legacy_code.py
# - запустить task1_main.py и убедиться, что код работает как и раньше (нет exception)
# - проверить папку с файлами mypy --strict и убедиться, что нет ошибок

from types import MappingProxyType
from urllib.parse import urlencode

NETBOX_URL = "https://demo.netbox.dev"


EXAMPLE_INPUT = MappingProxyType(
    {
        "manufacturer": ["cisco"],
        "role": ["router", "core-switch", "access-switch"],
        "status": ["active", "offline"],
        "site": ["dm-akronsk", "dm-albany", "dm-camden"],
    },
)
EXAMPLE_RESULT = (
    ("manufacturer_id", 3),
    ("role_id", 1),
    ("role_id", 2),
    ("role_id", 4),
    ("status", "active"),
    ("status", "offline"),
    ("site_id", 2),
    ("site_id", 3),
    ("site_id", 6),
    ("brief", "true"),
    ("limit", 500),
)


if __name__ == "__main__":
    result = craft_nb_query(EXAMPLE_INPUT)
    assert tuple(result) == EXAMPLE_RESULT, "функция 'craft_nb_query' работает некорректно"
    print(f"{NETBOX_URL}/api/dcim/devices/?{urlencode(result)}")
