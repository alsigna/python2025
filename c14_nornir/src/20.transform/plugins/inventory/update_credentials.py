import os

from nornir.core.inventory import Host


def update_credentials(host: Host) -> None:
    # export SSH_USERNAME=admin SSH_PASSWORD=P@ssw0rd
    host.username = os.getenv("SSH_USERNAME")
    host.password = os.getenv("SSH_PASSWORD")
