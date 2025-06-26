from functools import partial


class NetboxObjectResolver:
    """Класс для преобразования параметров запроса в список params для Netbox API."""

    SITE_IDS = {
        "dm-akronsk": 2,
        "dm-albany": 3,
        "dm-binghamton": 4,
        "dm-buffalo": 5,
        "dm-camden": 6,
    }
    ROLE_IDS = {
        "router": 1,
        "core-switch": 2,
        "distribution-switch": 3,
        "access-switch": 4,
    }
    MANUFACTURER_IDS = {
        "arista": 1,
        "cisco": 3,
        "juniper": 7,
    }

    @classmethod
    def get_site_id(cls, site_slug):
        """Заглушка для получения id сайта по его slug."""
        site_id = cls.SITE_IDS.get(site_slug)
        if site_id is None:
            raise ValueError(f"неизвестный сайт '{site_slug}'")
        return ("site_id", site_id)

    @classmethod
    def get_role_id(cls, role_slug):
        """Заглушка для получения id роли устройства по её slug."""
        role_id = cls.ROLE_IDS.get(role_slug)
        if role_id is None:
            raise ValueError(f"неизвестная роль устройства '{role_slug}'")
        return ("role_id", role_id)

    @classmethod
    def get_manufacturer_id(cls, manufacturer_slug):
        """Заглушка для получения id производителя по его slug."""
        manufacturer_id = cls.MANUFACTURER_IDS.get(manufacturer_slug)
        if manufacturer_id is None:
            raise ValueError(f"неизвестный производитель '{manufacturer_slug}'")
        return ("manufacturer_id", manufacturer_id)

    @classmethod
    def get_name_ie(cls, name):
        """Добавляет имя как параметр с регистро-независимым точным поиском (ie)."""
        return ("name__ie", name.lower())

    @classmethod
    def get_status(cls, status):
        """Добавляет статус как параметр."""
        return ("status", status.lower())


def process_items(processor, items):
    """Применяет процессор к каждому элементу последовательности."""
    return [processor(item) for item in items]


def craft_nb_query(request_params):
    """Преобразование набора параметров в request params.

    Args:
        request_params (dict[str, str]): параметры запроса.
        ```python
        {
            "manufacturer": ["cisco"],
            "role": ["router"],
            "status": ["active", "offline"],
            "site": ["dm-akronsk", "dm-albany"],
        }
        ```

    Raises:
        ValueError: если переданы неизвестные или пустые параметры

    Returns:
        type QueryParam = tuple[str, str | int]
        list[QueryParam]: список кортежей из переданных параметров + brief и limit:
        ```python
        [
            ("manufacturer_id", 3),
            ("role", "router"),
            ("status", "active"),
            ("status", "offline"),
            ("site_id", 2),
            ("site_id", 3),
            ("brief", "true"),
            ("limit", 500),
        ]
        ```
    """
    if len(request_params) == 0:
        raise ValueError("отсутствуют параметры запроса")

    item_type_map = {
        "name": partial(process_items, NetboxObjectResolver.get_name_ie),
        "site": partial(process_items, NetboxObjectResolver.get_site_id),
        "role": partial(process_items, NetboxObjectResolver.get_role_id),
        "manufacturer": partial(process_items, NetboxObjectResolver.get_manufacturer_id),
        "status": partial(process_items, NetboxObjectResolver.get_status),
    }
    q = []
    for item_type, items in request_params.items():
        expose_func = item_type_map.get(item_type)
        if expose_func is None:
            raise ValueError("неизвестный тип параметра")
        q.extend(expose_func(items))

    q.append(("brief", "true"))
    q.append(("limit", 500))
    return q
