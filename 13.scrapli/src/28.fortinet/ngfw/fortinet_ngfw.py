from scrapli.driver.network.base_driver import PrivilegeLevel
from scrapli_community.fortinet.ngfw.async_driver import default_async_on_close, default_async_on_open
from scrapli_community.fortinet.ngfw.sync_driver import default_sync_on_close, default_sync_on_open

DEFAULT_PRIVILEGE_LEVELS = {
    "privilege_exec": (
        PrivilegeLevel(
            pattern=r"[\w_-]+ (\([\w-]+\) )?#",
            name="privilege_exec",
            previous_priv="",
            deescalate="",
            escalate="",
            escalate_auth=False,
            escalate_prompt="",
        )
    ),
}

SCRAPLI_PLATFORM = {
    "driver_type": "network",
    "defaults": {
        "privilege_levels": DEFAULT_PRIVILEGE_LEVELS,
        "default_desired_privilege_level": "privilege_exec",
        "sync_on_open": default_sync_on_open,
        "async_on_open": default_async_on_open,
        "sync_on_close": default_sync_on_close,
        "async_on_close": default_async_on_close,
        "failed_when_contains": [
            "Command fail",
            "Unknown action",
            "is not unique",
            "Unrecognized command",
            "Insufficient parameters for command",
            "Error:",
        ],
        "textfsm_platform": "",
        "genie_platform": "",
    },
}
