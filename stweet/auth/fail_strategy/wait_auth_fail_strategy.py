import time

from stweet.auth.fail_strategy.auth_fail_strategy import AuthFailStrategy


class WaitAuthFailStrategy(AuthFailStrategy):
    ms_wait: int

    def __init__(self, ms_wait: int):
        self.ms_wait = ms_wait

    def run_strategy(self) -> None:
        time.sleep(self.ms_wait * 1.0 / 1000)
