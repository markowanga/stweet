import time

from tor_python_easy.tor_control_port_client import TorControlPortClient

from stweet.auth.fail_strategy.auth_fail_strategy import AuthFailStrategy


class TorIpChangeAuthFailStrategy(AuthFailStrategy):
    tor_control_port_client: TorControlPortClient

    def __init__(self, tor_control_port_client: TorControlPortClient):
        self.tor_control_port_client = tor_control_port_client

    def run_strategy(self) -> None:
        time.sleep(5)
        self.tor_control_port_client.change_connection_ip()
