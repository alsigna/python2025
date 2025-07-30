"""scrapli_community.eltex.esr.sync_driver"""

from scrapli.driver import NetworkDriver


def default_sync_on_close(conn: NetworkDriver) -> None:
    conn.channel.write(channel_input="config system console")
    conn.channel.send_return()
    conn.channel.write(channel_input="set output more")
    conn.channel.send_return()
    conn.channel.write(channel_input="end")
    conn.channel.send_return()
    conn.channel.write(channel_input="quit")
    conn.channel.send_return()

def default_sync_on_open(conn: NetworkDriver) -> None:
    conn.channel.write(channel_input="config system console")
    conn.channel.send_return()
    conn.channel.write(channel_input="set output standard")
    conn.channel.send_return()
    conn.channel.write(channel_input="end")
    conn.channel.send_return()

