from abc import ABC, abstractmethod

class Screen(ABC):
    @abstractmethod
    def type(self) -> str:
        pass

    @abstractmethod
    def handle(self) -> 'Screen':
        pass


class MainMenu(Screen):
    def type(self) -> str:
        return "Main Menu"

    def handle(self) -> 'Screen':
        pass


class UI:
    def __init__(self
                 ):
        self.screen = ScreenType.MainMenu

    def run(self):


