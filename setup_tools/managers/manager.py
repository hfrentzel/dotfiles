from abc import ABC, abstractmethod


class Manager(ABC):
    def __init_subclass__(cls):
        cls._requested = set()
        cls._missing = set()

    @classmethod
    @abstractmethod
    async def update(cls):
        pass
