from abc import abstractmethod, ABC
import dearpygui.dearpygui as dpg
from typing import Type
from typing import Callable, Optional


class IWindow(ABC):
    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @name.getter
    def name(self) -> str:
        return self.name

    @abstractmethod
    def create(self):
        pass

    def show(self):
        dpg.configure_item(self.name, show=True)

    def hide(self):
        dpg.configure_item(self.name, show=False)

    def set_primary(self):
        dpg.set_primary_window(self.name, True)

    # @abstractmethod
    # def update(self) -> Optional["IWindow"]:
    #     pass


class ReadDataInterface:
    pass


class RecordingWindow(IWindow):
    @property
    def name(self):
        self._name = "RecordingWindow"

    def __init__(self, read: ReadDataInterface):
        self._name = "RecordingWindow"
        self._read = read

    def _goto_window_callback(self, new_window: Type[IWindow]):
        RecordingWindow.show(new_window)
        RecordingWindow.set_primary(new_window)
        self.hide()

    def create(self):
        with dpg.window(tag=self._name):
            dpg.add_text("Live Session View")
            dpg.add_button(label="Home", callback=lambda: self._goto_window_callback(WelcomeWindow))


class IFileSelector(ABC):
    def get_file_from_user(self, starting_dir: str):
        pass


class DearPyGuiSelector(IFileSelector):
    def __init__(self, parent_window):
        self._parent = parent_window

    def get_file_from_user(self, starting_dir: str):
        # I didn't look up how this works
        with self._parent:
            # probably maybe use Modal instead???
            dpg.add_file_dialog(directory_selector=True, show=True, )


class SelectRecordingFileUseCase:
    def __init__(self, selector: IFileSelector):
        self._selector = selector

    def get_file(self, base_path: str) -> str:
        file = self._selector.get_file_from_user(base_path)
        if file not exists:
            file.create()
        return file.name


class WelcomeWindow(IWindow):
    @property
    def name(self):
        self._name = "WelcomeWindow"

    def __init__(self):
        self._name = "WelcomeWindow"

    def _goto_window_callback(self, new_window: Type[IWindow]):
        RecordingWindow.show(new_window)
        RecordingWindow.set_primary(new_window)
        self.hide()

    def create(self):
        with dpg.window(tag=self._name):
            dpg.add_text("Welcome")
            dpg.add_button(label="Record a new session", callback=lambda: self._goto_window_callback(RecordingWindow))
