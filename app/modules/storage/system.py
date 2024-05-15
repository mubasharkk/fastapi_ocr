from abc import ABC, abstractmethod


class StorageSystem(ABC):
    @abstractmethod
    def put(self, key: str):
        pass

    @abstractmethod
    def put_data(self, data):
        pass

    def read(self, key: str) -> str:
        pass

    def exists(self, key: str) -> bool:
        pass
