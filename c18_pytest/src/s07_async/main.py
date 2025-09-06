import asyncio

from netbox_api_handler import NetboxAPIHandler

NETBOX_TOKEN = "d5562616b529e6a121805ecadffaf5c2f48aeeac"
NETBOX_URL = "https://demo.netbox.dev"
PARAMS = [
    ("brief", "true"),
]


async def amain() -> None:
    async with NetboxAPIHandler(NETBOX_URL, NETBOX_TOKEN) as netbox:
        roles, types, sites = await asyncio.gather(
            asyncio.create_task(netbox.aget("/api/dcim/device-roles/", PARAMS)),
            asyncio.create_task(netbox.aget("/api/dcim/device-types/", PARAMS)),
            asyncio.create_task(netbox.aget("/api/dcim/sites/", PARAMS)),
        )

        print({role["slug"]: role["id"] for role in roles})
        print({type_["slug"]: type_["id"] for type_ in types})
        print({site["slug"]: site["id"] for site in sites})


def main() -> None:
    with NetboxAPIHandler(NETBOX_URL, NETBOX_TOKEN) as netbox:
        roles = netbox.get("/api/dcim/device-roles/", PARAMS)
        types = netbox.get("/api/dcim/device-types/", PARAMS)
        sites = netbox.get("/api/dcim/sites/", PARAMS)

        print({role["slug"]: role["id"] for role in roles})
        print({type_["slug"]: type_["id"] for type_ in types})
        print({site["slug"]: site["id"] for site in sites})


if __name__ == "__main__":
    main()
    print("-" * 10)
    asyncio.run(amain())
