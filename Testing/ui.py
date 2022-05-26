from abc import ABC, abstractmethod


class Screen(ABC):
    @abstractmethod
    def type(self) -> str:
        pass

    @abstractmethod
    def handle(self) -> 'Screen':
        pass


class WelcomeScreen(Screen):
    def type(self) -> str:
        return "Welcome Screen"

    def handle(self) -> 'Screen':
        pass


class UI:
    def __init__(self):
        self.screen = ScreenType.WelcomeScreen

    def run(self):
