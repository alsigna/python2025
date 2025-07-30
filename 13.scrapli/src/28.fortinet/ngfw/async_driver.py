"""scrapli_community.eltex.esr.async_driver"""

from scrapli.driver import AsyncNetworkDriver


async def default_async_on_close(conn: AsyncNetworkDriver) -> None:
    conn.channel.write(channel_input="config system console")
    conn.channel.send_return()
    conn.channel.write(channel_input="set output more")
    conn.channel.send_return()
    conn.channel.write(channel_input="end")
    conn.channel.send_return()
    conn.channel.write(channel_input="quit")
    conn.channel.send_return()

async def default_async_on_open(conn: AsyncNetworkDriver) -> None:
    conn.channel.write(channel_input="config system console")
    conn.channel.send_return()
    conn.channel.write(channel_input="set output standard")
    conn.channel.send_return()
    conn.channel.write(channel_input="end")
    conn.channel.send_return()

