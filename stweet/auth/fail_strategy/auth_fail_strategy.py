from abc import ABC, abstractmethod


class AuthFailStrategy(ABC):

    @abstractmethod
    def run_strategy(self) -> None:
        pass
