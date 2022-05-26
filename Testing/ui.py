from abc import ABC, abstractmethod


class Window(ABC):
    @abstractmethod
    def type(self) -> str:
        pass

    @abstractmethod
    def handle(self) -> 'Window':
        pass


class WelcomeWindow(Window):
    def type(self) -> str:
        return "Welcome Window"

    def handle(self) -> 'Window':
        pass


class UI:
    def __init__(self):
        self.window = WindowType.WelcomeWindow

    def run(self):
