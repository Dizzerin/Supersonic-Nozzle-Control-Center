from abc import ABC, abstractmethod


# Abstract base class which all windows implement
class IWindow(ABC):
    @staticmethod
    @abstractmethod
    def tag() -> str:
        pass

    @abstractmethod
    def create(self) -> 'Window':
        pass
